# -*- coding: utf-8 -*-

'''
    File name: core.py
    Python Version: 3.6
'''
import multiprocessing

from netCDF4._netCDF4 import Dataset, date2num

__author__ = "Igor Lima"
__version__ = "0.1"
__email__ = "igor.santos@climatempo.com"
__status__ = "Development"

# Tag das Mensagens:
# [I] -> Informacao
# [A] -> Aviso/Alerta
# [E] -> Erro

from datetime import datetime
import os

import pandas
import numpy as np


class IDW():

    def __init__(self, data, latini, latfim, lonini, lonfim, resolution=None, power=None, radius_influence=None,
                 verbose=False):
        self.latini = latini
        self.latfim = latfim
        self.lonini = lonini
        self.lonfim = lonfim
        self.data = data
        self.resolution = resolution
        self.power = power
        self.radius_influence = radius_influence
        if self.power is None: self.power = 2
        if self.resolution is None: self.resolution = 0.09
        if self.radius_influence is None: self.radius_influence = 0.5

    def interpolate(self):

        self.data = self.data[(self.data.chuva >= 0) & (self.data.chuva < 500)]
        itime = np.array(sorted(self.data.dia.unique()))


        NC = abs(round(((self.lonfim - self.lonini) / self.resolution) + 1))
        NL = abs(round(((self.latfim - self.latini) / self.resolution) + 1))


        new_lat = [self.latini + i * self.resolution for i in range(0, NL)]
        new_lon = [self.lonini + i * self.resolution for i in range(0, NC)]

        nx = 0
        ny = 0

        valp = np.ones((len(itime), NL, NC)) * -99
        ri = round(self.radius_influence / self.resolution)

        try:

            for time_index, dia in np.ndenumerate(itime):
                sval = np.zeros((NL, NC))
                sdist = np.zeros((NL, NC))
                new = self.data[self.data.dia == dia]
                latitude = np.array(new.lat)
                longitude = np.array(new.lon)
                chuva = np.array(new.chuva)

                for ix in range(len(latitude)):

                    if latitude[ix] <= self.latfim and latitude[ix] >= self.latini and longitude[ix] <= self.lonfim and \
                            longitude[
                                ix] >= self.lonini:

                        # Menor indice entre a latittude e longitude atual
                        for i in range(0, NL):
                            if abs(latitude[ix] - new_lat[i]) < self.resolution: ny = i
                        for j in range(0, NC):
                            if abs(longitude[ix] - new_lon[j]) < self.resolution: nx = j

                        ii = ny - ri
                        ie = ny + ri
                        if ii < 0: ii = 0
                        if ie > NL: ie = NL

                        ji = nx - ri
                        je = nx + ri
                        if ji < 0: ji = 0
                        if je > NC: je = NC

                        for il in range(ii, ie):
                            for jl in range(ji, je):
                                if chuva[ix] >= 0:

                                    dist = (longitude[ix] - new_lon[jl]) ** 2 + (latitude[ix] - new_lat[il]) ** 2
                                    if dist == 0: dist = 0.0001
                                    if dist <= self.radius_influence:
                                        sdist[il, jl] = sdist[il, jl] + (1 / dist ** self.power)
                                        sval[il, jl] = sval[il, jl] + (chuva[ix] / dist ** self.power)

                for ix in list(zip(*np.where(sdist > 0))):
                    valp[time_index, ix[0], ix[1]] = sval[ix[0], ix[1]] / sdist[ix[0], ix[1]]

            return new_lat, new_lon, itime, valp

        except Exception as e:
            print('[E.{dt:%Y%m%d%H%M}][PID.{pid}] IDW.interpolate >>  {e}'.format(
                dt=datetime.now(),
                pid=os.getpid(),
                e=e
            ))

