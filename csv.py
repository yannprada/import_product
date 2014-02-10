# -*- coding: utf-8 -*-
#!/usr/bin/python

import csv


def format(fileName, keys=None, input_kwargs=None):
    '''
someFile: a file name
return: list of objects with columns names as attributes
    '''
    if not input_kwargs:
        input_kwargs = {
            'delimiter': ';',
            'quotechar': "'",
            'quoting': csv.QUOTE_MINIMAL,
            'lineterminator': '\n',
        }

