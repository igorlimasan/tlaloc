# -*- coding: utf-8 -*-

'''
    File name: core.py
    Python Version: 3.6
'''
import pandas
from netCDF4 import Dataset, date2num
from tlaloc.settings import BASE_DIR
__author__ = ""
__version__ = "0.1"
__email__ = ""
__status__ = "Development"


# Tag das Mensagens:
# [I] -> Informacao
# [A] -> Aviso/Alerta
# [E] -> Erro
def datahubSave(prec, itime, new_lat, new_lon):

    # lista com todos os valores de tempo interpolados

    chuva_file = Dataset(BASE_DIR+'/tlaloc/output/chuva_interpolada.nc', 'w', format='NETCDF4')

    # idx é quantidade de pontos de longitude, idy é a quantidade de pontos de latitude e it é a quantidade de
    # pontos de tempo
    it = len(itime)

    # RLONv calcula uma lista de longitude dentro do bounding box e RLATv calcula uma lista de latitudes dentro do
    # bounding box

    chuva_file.createDimension("lat", len(new_lat))
    chuva_file.createDimension("lon", len(new_lon))
    chuva_file.createDimension("level", 1)
    chuva_file.createDimension("time", it)

    _horario = chuva_file.createVariable("time", "i4", ("time",))
    _latitude = chuva_file.createVariable("lat", "f4", ("lat",))
    _longitude = chuva_file.createVariable("lon", "f4", ("lon",))
    _level = chuva_file.createVariable("level", "f4", ("level",))
    _chuva = chuva_file.createVariable("chuva", "f4", ("time", "level", "lat", "lon",), fill_value=-99)

    _horario.units = 'days since 1970-01-01 00:00:00'
    _chuva.units = 'mm'
    _chuva.long_name = 'precipitacao'
    _latitude.axis = 'Y'
    _latitude.units = 'degrees_north'
    _latitude.long_name = 'latitude'
    _longitude.axis = 'X'
    _longitude.units = 'degrees_east'
    _longitude.long_name = 'longitude'

    for ix_time in range(it):
        # for x in range(len(new_lon)):
        #     for y in range(len(new_lat)):
        _chuva[ix_time, 0, :, :] = prec[ix_time, :, :]

    _horario[:] = date2num(pandas.to_datetime(itime).astype(object).values, 'days since 1970-01-01 00:00:00')
    _longitude[:] = new_lon
    _latitude[:] = new_lat
    _chuva[:, :, :, :] = _chuva[:, :, :, :]
    _level[:] = 0

    # print('[I] AreaReport.__create_netcdf >> Arquivo em NetCDF criado com sucesso: {}'.format(_file))

    chuva_file.close()
