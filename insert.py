# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager
from table import Table


def main(host, database, password, fileName):
    m = Manager(host, database, password)
    
    product_categ = Table('product.category', m)
    product_tmpl = Table('product.template', m)
    product_product = Table('product.product', m)
    ir_model_data = Table('ir.model.data', m)
    
    def getID(args, table):
        ids = table.search(args)
        return ids[0] if len(ids) > 0 else False
    
    def getCategID(name):
        return getID([('name', '=', name)], product_categ)
    
    def insertOrUpdate(ref, model, data):
        '''
    Check the table ir_model_data to see if the ref exist, then insert or update in the given model.
    ref: external reference
    model: model related
    data: data to insert/update
    return: id
        '''
        ir_model_data_id = getID([('name', '=', ref), ('model', '=', model.name)], ir_model_data)
        if ir_model_data_id:
            ir_model_data_result = ir_model_data.read([ir_model_data_id], ['res_id'])
            model_id = ir_model_data_result[0]['res_id']
            model.write([model_id], data)
        else:
            model_id = model.create(data)
            data_model = {
                'name': ref,
                'model': model.name,
                'res_id': model_id,
            }
            ir_model_data_id = ir_model_data.create(data_model)
        
        return model_id
    
    
    c = CsvParser(fileName, delimiter=';')
    # insert in:
    #     product.template
    #     product.product
    #     ir.model.data
    total = len(c.rows)
    count = 0
    for row in c.rows:
        count += 1
        
        data_tmpl = {
            'list_price': row['prix_vente_ht'],
            'description': row['description'],
            'weight_net': row['poids_net'],
            'standard_price': row['prix_achat_ht'],
            'categ_id': getCategID(row['categorie']),
            'name': row['nom'],
            'sale_ok': True,
            'type': row['type'],
            'supply_method': 'buy',
            'procure_method': 'make_to_stock',
            'purchase_ok': True,
        }
        
        ref = row['reference'] + '_product_template'
        product_tmpl_id = insertOrUpdate(ref, product_tmpl, data_tmpl)
        
        data_product = {
            'default_code': row['reference'],
            'name_template': row['nom'],
            'active': True,
            'product_tmpl_id': product_tmpl_id,
        }
        
        ref = row['reference']
        product_product_id = insertOrUpdate(ref, product_product, data_product)
        
        if __name__ == '__main__':
            print(str(count) + '/' + str(total))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
    Usage:
        python insert.py [host] [database] [password] [file.csv]
    ''')
        sys.exit()
    else:
        t1 = time.time()
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

