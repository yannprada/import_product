# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager
from table import Table


class ProductManager(Manager):
    def __init__(self, host, dbname, password):
        super(ProductManager, self).__init__(host, dbname, password)
        self.product_categ = Table('product.category', self)
        self.product_tmpl = Table('product.template', self)
        self.product_product = Table('product.product', self)
        self.ir_model_data = Table('ir.model.data', self)
    
    def getID(self, args, table):
        ids = table.search(args)
        return ids[0] if len(ids) > 0 else False
    
    def getCategID(self, name):
        return self.getID([('name', '=', name)], self.product_categ)
    
    def insertOrUpdate(self, ref, model, data):
        '''
Check the table ir_model_data to see if the ref exist, then insert or update in the given model.
ref: external reference
model: model related
data: data to insert/update
return: id
        '''
        ir_model_data_id = self.getID([('name', '=', ref), ('model', '=', model.name)], self.ir_model_data)
        if ir_model_data_id:
            result = self.ir_model_data.read([ir_model_data_id], ['res_id'])
            model_id = result[0]['res_id']
            model.write([model_id], data)
        else:
            model_id = model.create(data)
            data_model = {
                'name': ref,
                'model': model.name,
                'res_id': model_id,
            }
            ir_model_data_id = self.ir_model_data.create(data_model)
        return model_id
    
    def run(self, fileName):
        c = CsvParser(fileName, delimiter=';')
        # insert in:
        #     product.template
        #     product.product
        #     ir.model.data
        count = 0
        for row in c.rows:
            count += 1
            
            data_tmpl = {
                'list_price': row['prix_vente_ht'],
                'description': row['description'],
                'weight_net': row['poids_net'],
                'standard_price': row['prix_achat_ht'],
                'categ_id': self.getCategID(row['categorie']),
                'name': row['nom'],
                'sale_ok': True,
                'type': row['type'],
                'supply_method': 'buy',
                'procure_method': 'make_to_stock',
                'purchase_ok': True,
            }
            
            ref = row['reference'] + '_product_template'
            product_tmpl_id = self.insertOrUpdate(ref, self.product_tmpl, data_tmpl)
            
            data_product = {
                'default_code': row['reference'],
                'name_template': row['nom'],
                'active': True,
                'product_tmpl_id': product_tmpl_id,
            }
            
            ref = row['reference']
            product_product_id = self.insertOrUpdate(ref, self.product_product, data_product)
            
            if __name__ == '__main__':
                print(str(count) + '/' + str(c.total))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
    Usage:
        python insert.py [host] [database] [password] [file.csv]
    ''')
        sys.exit()
    else:
        t1 = time.time()
        pm = ProductManager(sys.argv[1], sys.argv[2], sys.argv[3])
        pm.run(sys.argv[4])
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

