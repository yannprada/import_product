# -*- coding: utf-8 -*-
#!/usr/bin/python

import csv


class CsvParser(object):
    '''
CsvParser
=======

Parse a csv file.
    '''
    def __init__(self, fileName, fieldNames=None, **input_kwargs):
        if not input_kwargs:
            input_kwargs = {
                'delimiter': ',',
                'quotechar': "'",
                'quoting': csv.QUOTE_MINIMAL,
                'lineterminator': '\n',
            }
        self.input_kwargs = input_kwargs
        self.fieldNames = fieldNames
        self.fileName = fileName
    
    def rows(self):
        with open(self.fileName, 'r') as csvFile:
            reader = csv.DictReader(csvFile, self.fieldNames, **self.input_kwargs)
            for row in reader:
                yield row, reader.line_num

