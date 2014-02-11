# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
from csv_parser import CsvParser
from manager import Manager
from table import Table

if len(sys.argv) < 5:
    print('''
Usage:
    python insert.py [host] [database] [password] [file.csv]
''')
    sys.exit()


m = Manager(sys.argv[1], sys.argv[2], sys.argv[3])
product_categ = Table('product.category', m)
product_tmpl = Table('product.template', m)
product_product = Table('product.product', m)
ir_model_data = Table('ir.model.data', m)

def getID(args, table):
    ids = table.search(args)
    return ids[0] if len(ids) > 0 else False

def getCategID(name):
    return getID([('name', '=', name)], product_categ)

def refExist(ref, model):
    '''
Check the table ir_model_data to see if the ref exist
ref: external reference
model: model related
return: id if exist, else False
    '''
    return getID([('name', '=', ref), ('model', '=', model)], ir_model_data)


c = CsvParser(sys.argv[4], delimiter=';')
# insert in:
#     product.template
#     product.product
#     ir.model.data
total = len(c.rows)
count = 0
for row in c.rows:
    count += 1
    print(str(count) + '/' + str(total))
    
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
    model = product_tmpl.name
    product_tmpl_id = refExist(ref, model)
    
    if product_tmpl_id != False:
        product_tmpl.write([product_tmpl_id], data_tmpl)
    else:
        product_tmpl_id = product_tmpl.create(data_tmpl)
        data_model = {
            'name': ref,
            'model': model,
            'res_id': product_tmpl_id,
        }
        ir_model_data_id = ir_model_data.create(data_model)
    
    data_product = {
        'default_code': row['reference'],
        'name_template': row['nom'],
        'active': True,
        'product_tmpl_id': product_tmpl_id,
    }
    
    ref = row['reference']
    model = product_product.name
    product_product_id = refExist(ref, model)
    
    if product_product_id:
        product_product.write([product_product_id], data_product)
    else:
        product_product_id = product_product.create(data_product)
        data_model = {
            'name': ref,
            'model': model,
            'res_id': product_product_id,
        }
        ir_model_data_id = ir_model_data.create(data_model)

