# -*- coding: utf-8 -*-

'''
    File name: service.py
    Python Version: 3.6.0
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
import sys
import multiprocessing
from datetime import datetime

import argparse

import controller

processes_number = int(multiprocessing.cpu_count())
parser = argparse.ArgumentParser(description='''
Descricao:
------------

''', formatter_class=argparse.RawTextHelpFormatter)

# parser.add_argument("--dates", dest='date_filter', type=str, action='store', nargs=2,
#                     help='Selecionar periodo particular de datas [YYYYMMDDHHMM_inicial, YYYYMMDDHHMM_final]')

parser.add_argument("-v", "--verbose", action='store_true', dest='verbose', help="Verbose", default=False)

parser.add_argument("-c", "--configure", type=str, dest='configure',
                    help="Configuração de inicialização. ", default=None)

parser.add_argument("-f", "--file", type=str, dest='file_path',
                    help="Arquivo com os dados. ", default=None)



args = parser.parse_args()

if __name__ == "__main__":
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("[I][PID.{}] Inicio - {} ({}).".format(os.getpid(), now, sys.argv[0]))

    controller.run(configure=args.configure,file_path = args.file_path,  verbose=args.verbose)

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("[I][PID.{}] Fim - {} ({}).".format(os.getpid(), now, sys.argv[0]))
    sys.exit(0)
