# -*- coding: utf-8 -*-
#!/usr/bin/python

import xmlrpclib


class Manager(object):
    '''
Manager
=======

Manage the insertion of data into a database.
    '''
    def __init__(self, host, dbname, password):
        self.sock = xmlrpclib.ServerProxy(host + '/xmlrpc/object')
        self.uid = 1
        self.db = dbname
        self.pwd = password
    
    def dbaction(self, tableName, action, arg1, arg2=None):
        '''
tableName: the name of the table
action: the action to execute
arg1: first argument
arg2: second argument
        '''
        if arg2 == None:
            return self.sock.execute(self.db, self.uid, self.pwd, tableName, action, arg1)
        else:
            return self.sock.execute(self.db, self.uid, self.pwd, tableName, action, arg1, arg2)

