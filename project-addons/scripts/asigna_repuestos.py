#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xmlrpclib
import socket
import traceback
import xlrd

class asigna_repuestos(object):
    def __init__(self, dbname, user, passwd):
        """método incial"""

        try:
            self.url_template = "http://%s:%s/xmlrpc/%s"
            self.server = "localhost"
            self.port = 8069
            self.dbname = dbname
            self.user_name = user
            self.user_passwd = passwd

            #
            # Conectamos con OpenERP
            #
            login_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'common'))
            self.user_id = login_facade.login(self.dbname, self.user_name, self.user_passwd)
            self.object_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'object'))

            res = self.asigna_repuestos()
            #con exito
            if res:
                print ("All created")
        except Exception, e:
            print ("ERROR: ", (e))
            sys.exit(1)

        #Métodos Xml-rpc

    def exception_handler(self, exception):
        """Manejador de Excepciones"""
        print "HANDLER: ", (exception)
        return True

    def create(self, model, data, context={}):
        """
        Wrapper del metodo create.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                            model, 'create', data, context)
            return res
        except socket.error, err:
            raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en create: %s' % (err.faultCode, err.faultString))


    def search(self, model, query, offset=0, limit=False, order=False, context={}, count=False, obj=1):
        """
        Wrapper del metodo search.
        """
        try:
            ids = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                    model, 'search', query, offset, limit, order, context, count)
            return ids
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception(u'Error %s en search: %s' % (err.faultCode, err.faultString))


    def read(self, model, ids, fields, context={}):
        """
        Wrapper del metodo read.
        """
        try:
            data = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                            model, 'read', ids, fields, context)
            return data
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception(u'Error %s en read: %s' % (err.faultCode, err.faultString))


    def write(self, model, ids, field_values,context={}):
        """
        Wrapper del metodo write.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                    model, 'write', ids, field_values, context)
            return res
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception(u'Error %s en write: %s' % (err.faultCode, err.faultString))


    def unlink(self, model, ids, context={}):
        """
        Wrapper del metodo unlink.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                    model, 'unlink', ids, context)
            return res
        except socket.error, err:
                raise Exception(u'Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                    raise Exception(u'Error %s en unlink: %s' % (err.faultCode, err.faultString))

    def default_get(self, model, fields_list=[], context={}):
        """
        Wrapper del metodo default_get.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                        model, 'default_get', fields_list, context)
            return res
        except socket.error, err:
                raise Exception('Conexion rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception('Error %s en default_get: %s' % (err.faultCode, err.faultString))

    def execute(self, model, method, *args, **kw):
        """
        Wrapper del método execute.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                                                model, method, *args, **kw)
            return res
        except socket.error, err:
                raise Exception('Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
                raise Exception('Error %s en execute: %s' % (err.faultCode, err.faultString))

    def exec_workflow(self, model, signal, ids):
        """ejecuta un workflow por xml rpc"""
        try:
            res = self.object_facade.exec_workflow(self.dbname, self.user_id, self.user_passwd, model, signal, ids)
            return res
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en exec_workflow: %s' % (err.faultCode, err.faultString))

    def _get_stateId_byName(self, state_name):
        state_ids = self.search("res.country.state", [('name','ilike',state_name)])
        return state_ids and state_ids[0] or False

    def _getPartnerCategories(self, *args):
        by_default_values = ["SIN CATEGORIZAR","ZZ - No informado"]
        category_ids = []
        for arg in args:
            if arg and arg not in by_default_values:
                categ_ids = self.search("res.partner.category", [("name",'=',arg)])
                if categ_ids:
                    category_ids.append(categ_ids[0])
                else:
                    categ_id = self.create("res.partner.category", {"name": arg})
                    category_ids.append(categ_id)
        return [(6,0,category_ids)]

    def asigna_repuestos(self):
       
        product_ids = self.search("product.product", [("categ_id", 'child_of',118 ),('default_code','like','%-%'),('replacement_ids', '!=', False)])
        tot =len(product_ids)
        print "TOTAL a COPIAR: " + str(tot)
        cont=0
        #all_lines = sh.nrows - 1
        #print "products no: ", all_lines

        #try:
        for product_id in product_ids:
            product_data = self.read("product.product", product_id, ["default_code", "replacement_ids", "categ_id"])
            print product_data
            code_to_find = product_data["default_code"].split('-',1)[0]
            print product_data["default_code"]
            print code_to_find
            products_to_update = self.search("product.product", [("categ_id", 'child_of',118 ),('default_code','like',code_to_find+'%'),('replacement_ids', '=', False)])
            #print products_to_update
            #product_data_to_update = self.read("product.product", products_to_update, ["default_code", "categ_id"])
            #print product_data_to_update
            if not (product_data["categ_id"]  in (125, 127, 241, 240) and product_data["default_code"][0] in ['B','Z']):
                self.write("product.product", products_to_update,
                            {'replacement_ids': [(6, 0,  product_data["replacement_ids"])]})
                print "ACTUALIZADO: " 
                print product_data["default_code"]
                print "para " 
                print products_to_update
                print "con"
                print  product_data["replacement_ids"]
                print "\n\n"
            else:
                print "IGNORADO: " + product_data["default_code"]
            #if record[6]:
                #products_ids = self.search("product.product", [("default_code", '=', int(record[6])),'|',('active','=',True),('active','=',False)])
                #if products_ids:
                    #product_data = self.read("product.product", products_ids[0], ["product_tmpl_id"])
                    #supp_ids = self.search("product.supplierinfo", [('product_tmpl_id', '=', product_data["product_tmpl_id"][0])])
                    #if supp_ids:
                        #self.write("product.supplierinfo", supp_ids, {'product_name': record[3]})

            #print "%s de %s" % (cont, all_lines)
            cont += 1
            print str(cont) + " de " + str(tot)
        #except Exception, e:
        #    print "EXCEPTION: REC: " 

        return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print u"Uso: %s <dbname> <user> <password>" % sys.argv[0]
    else:
        asigna_repuestos(sys.argv[1], sys.argv[2], sys.argv[3])
