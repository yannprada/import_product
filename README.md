import
======

xmlrpc script to insert products into an openerp 7 database

##TODO:

Make the code modular, example:
* split database inserts, csv formating in two functions (or classes)
* make this file a lib
* make another file which use the functions (in this case to insert products)

Three cases when inserting into a table:
* a simple value
* a many2one relation (need an id for a given value)
* a many2many relation (need two ids and a third table)