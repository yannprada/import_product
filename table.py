# -*- coding: utf-8 -*-
#!/usr/bin/python


class Table(object):
    '''
Relationnal data
================

Represents a relationnal table.
Can call db actions.
    '''
    def __init__(self, name, manager):
        self.name = name
        self._manager = manager
    
    def search(self, condition):
        '''
condition: a list of 3-uplets like [('name', '=', 'Miller')] or [('a', '>', 1),('b', '=', True)]
return: IDs
        '''
        return self._manager.dbaction(self.name, 'search', condition)
    
    def read(self, ids, fields):
        '''
ids: ids of rows requested
fields: a list of fields to display
return: a list of objects
        '''
        return self._manager.dbaction(self.name, 'read', ids, fields)
    
    def create(self, data):
        '''
data: an object which contains the data to use
return: the ID of the row created
        '''
        return self._manager.dbaction(self.name, 'create', data)
    
    def write(self, ids, data):
        '''
ids: ids where the update must be done
data: an object which contains the data to use
return: True if success
        '''
        return self._manager.dbaction(self.name, 'write', ids, data)
    
    def unlink(self, ids):
        '''
ids: ids where the unlink must be done
return: True if success
        '''
        return self._manager.dbaction(self.name, 'unlink', ids)

