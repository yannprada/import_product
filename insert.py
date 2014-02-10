# -*- coding: utf-8 -*-
#!/usr/bin/python

import xmlrpclib as xrl


class Table(object):
    '''
Relationnal data
================

Represents a relationnal table.
Can call db actions.
    '''
    def __init__(self, name, column, manager):
        self.name = name        # table name
        self.column = column    # column name of the table of which this table is related to
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
    
    def write(self, data, ids):
        '''
data: an object which contains the data to use
ids: ids where the update must be done
return: True if success
        '''
        return self._manager.dbaction(self.name, 'write', ids, data)
    
    def unlink(self, ids):
        '''
ids: ids where the unlink must be done
return: True if success
        '''
        return self._manager.dbaction(self.name, 'unlink', ids)


class Manager(object):
    '''
Manager
=======

Manage the insertion of data into a database.
    '''
    def __init__(self, host, dbname, password):
        self.sock = xrl.ServerProxy(host + '/xmlrpc/object')
        self.uid = 1
        self.db = dbname
        self.pwd = password
    
    def dbaction(self, tableName, action, ids=False, args=False):
        '''
table: a table instance
action: type of action (search, read, create, update or delete)
ids: required for read, update and delete
args: data for create, update, or args for search, read
return: result of the action
        '''
        return self.sock.execute(self.db, self.uid, self.pwd, tableName, action, ids, args)



m = Manager('http://172.16.1.73:8069', 'test', 'v1m3xc0m')
t = Table('res.partner', 'u', m)
d = {
    'name': 'test DBaction',
    'customer': '1',
    'is_company': '1',
}
ID = t.create(d)


