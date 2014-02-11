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
        
        with open(fileName, 'r') as csvFile:
            reader = csv.DictReader(csvFile, fieldNames, **input_kwargs)
            self.rows = [row for row in reader]


