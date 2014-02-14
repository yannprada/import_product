# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class ProductManager(Manager):
    def __init__(self, host, dbname, password):
        super(ProductManager, self).__init__(host, dbname, password)
        self.existing_prod_tmpl_records = self.prepare('product.template')
        self.existing_prod_prod_records = self.prepare('product.product')
    
    def prepare(self, model):
        '''
Search all the records in ir.model.data for a given model, then returns an object with ref as key and id as value.
        '''
        ids = self.search('ir.model.data', [('model', '=', model)])
        data = self.read('ir.model.data', ids, ['res_id', 'name'])
        result = {}
        for item in data:
            ref = item['name']
            ID = item['res_id']
            result[ref] = ID
        return result
    
    def getCategID(self, name):
        ids = self.search('product.category', [('name', '=', name)])
        return ids[0] if len(ids) > 0 else False
    
    def insertOrUpdate(self, ref, model, data, checkList):
        '''
Check the table ir_model_data to see if the ref exist, then insert or update in the given model.
ref: external reference
model: name of the related model
data: data to insert/update
return: id
        '''
        if ref in checkList:
            ID = checkList[ref]
            self.write(model, [ID], data)
        else:
            ID = self.create(model, data)
            data_model = {
                'name': ref,
                'model': model,
                'res_id': ID,
            }
            ir_model_data_id = self.create('ir.model.data', data_model)
        return ID
    
    def run(self, fileName):
        c = CsvParser(fileName, delimiter=';')
        # insert in:
        #     product.template
        #     product.product
        #     ir.model.data
        for row, count in c.rows():
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
            ref = row['reference']
            product_tmpl_id = self.insertOrUpdate(
                    ref + '_product_template','product.template', data_tmpl, self.existing_prod_tmpl_records)
            
            data_product = {
                'default_code': ref,
                'name_template': row['nom'],
                'active': True,
                'product_tmpl_id': product_tmpl_id,
            }
            product_product_id = self.insertOrUpdate(
                    ref, 'product.product', data_product, self.existing_prod_prod_records)
            
            if __name__ == '__main__':
                print(str(count))


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

