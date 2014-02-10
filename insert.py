# -*- coding: utf-8 -*-
#!/usr/bin/python

import xmlrpclib


class RelData(object):
    '''
Relationnal data
================

Represents a relationnal table.
Give an ID with a given attribute.
    '''
    def __init__(self, name, column, socket, dbname, user, password):
        self.name = name        # table name
        self.column = column    # column name of the table of which this table is related to
        self._socket = socket
        self._dbname = dbname
        self._user = user
        self._password = password
    
    def getIDs(self, condition):
        '''
condition: a 3-uplet like ('name', '=', 'Miller')
return: a list of IDs 
        '''
        return self._socket.execute(self._dbname, self._user, self._password, self.name, 'search', [condition])

