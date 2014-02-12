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
        self.sock = xmlrpclib.ServerProxy(host + '/xmlrpc/object', allow_none=True)
        self.uid = 1
        self.db = dbname
        self.pwd = password
    
    def search(self, model, args):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'search', args)    
    
    def read(self, model, ids, fields):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'read', ids, fields)    
    
    def create(self, model, data):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'create', data)    
    
    def write(self, model, ids, data):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'write', ids, data)    
    
    def unlink(self, model, ids):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'unlink', ids)

