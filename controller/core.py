# -*- coding: utf-8 -*-

'''
    File name: core.py
    Python Version: 3.6
'''

__author__ = ""
__version__ = "0.1"
__email__ = ""
__status__ = "Development"

# Tag das Mensagens:
# [I] -> Informacao
# [A] -> Aviso/Alerta
# [E] -> Erro

import os
import json
import multiprocessing
from json.decoder import JSONDecodeError
from datetime import datetime
from crawler.core import CSVCrawler
from interpolators.core import IDW
from datahub.core import datahubSave

def init_child(lock_):
    global lock
    lock = lock_


def run(configure: str, file_path=None, verbose=True):
    '''

    :param configure: File with configure process 
    :type configure: str 
    :param verbose: Verbose mode
    :type verbose: bool 
    :param parallel: Parallel mode
    :type parallel: bool 
    :param processes: Parallel mode
    :type processes: int 
    :return: bool
    '''

    # Init

    # Load Configure
    if os.path.exists(configure):
        try:
            configure = json.loads(open(configure, mode='r').read())
        except JSONDecodeError as e:
            print('[E.{dt:%Y%m%d%H%M}][PID.{pid}] controller.run >> Format Error @ JSONDecodeError {e}'.format(
                dt=datetime.now(),
                pid=os.getpid(),
                e=e
            ))
            return False

    # Add Verbose
    # for _configure in configure:
    #     _configure.update({'verbose': verbose})

    if file_path is not None:
        print('[I.{dt:%Y%m%d%H%M}][PID.{pid}] Crawler'.format(
            dt=datetime.now(),
            pid=os.getpid()

        ))
        crawlerSettings = configure['CrawlerSettings']
        crawler = CSVCrawler(file_path, crawlerSettings['separator'], crawlerSettings['fields'],
                             crawlerSettings['columns'], crawlerSettings['time_period'],
                             crawlerSettings['date_format'])

    result = crawler.run()

    if not result.empty:
        print('[I.{dt:%Y%m%d%H%M}][PID.{pid}] Interpolador'.format(
            dt=datetime.now(),
            pid=os.getpid()

        ))
        interpolator = IDW(result,configure['InterpolatorSettings']['box']['latini'],
                           configure['InterpolatorSettings']['box']['latfim'],
                           configure['InterpolatorSettings']['box']['lonini'],
                           configure['InterpolatorSettings']['box']['lonfim'],
                           configure['InterpolatorSettings']['degrees_resolution'],
                           configure['InterpolatorSettings']['power'],
                           configure['InterpolatorSettings']['radius_influence']
                           )
        new_lat,new_lon,itime,prec = interpolator.interpolate()
        datahubSave(prec,itime,new_lat,new_lon)



    else:
        print('[A.{dt:%Y%m%d%H%M}][PID.{pid}] controller.run >> Não há dados para concluir operação'.format(
                dt=datetime.now(),
                pid=os.getpid()))



    return False
