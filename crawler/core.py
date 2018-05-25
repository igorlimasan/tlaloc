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

import pandas


class CSVCrawler:
    def __init__(self, _path, separator, fields, columns, time_period, date_format):
        self._path = _path
        self.separator = separator
        self.fields = fields
        self.columns = columns
        self.time_period = time_period
        self.date_format = date_format

    def run(self):
        _data = pandas.read_csv(self._path, sep=self.separator)
        _data.rename(columns=dict(zip(self.columns, self.fields)))
        if self.time_period == 'hourly':
            _data.dia = pandas.to_datetime(_data.dia, format=self.date_format, errors='coerce')
            _data = _data[pandas.notnull(_data.dia)]
            _data.set_index('dia', inplace=True)
            _data = _data.groupby(['lat', 'lon', pandas.TimeGrouper('1h')])[
                'chuva'].sum().reset_index()

        else:
            _data.dia = pandas.to_datetime(_data.dia, format=self.date_format, errors='coerce')
            _data = _data[pandas.notnull(_data.dia)]
            _data.set_index('dia', inplace=True)
            _data = _data.groupby(['lat', 'lon', pandas.TimeGrouper('1D')])[
                'chuva'].sum().reset_index()



        return _data
