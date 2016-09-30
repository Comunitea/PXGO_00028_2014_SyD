#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xmlrpclib
import socket
import traceback
import xlrd

UOM_MAP = {'C': "Box(es)",
           'U': "Unit(s)",
           'K': "kg",
           'L': "Liter(s)"}
IVA_MAP = {
    "1": ["S_IVA10", "P_IVA10_BC"],
    "2": ["S_IVA4", "P_IVA4_BC"],
    "3": ["S_IVA21", "P_IVA21_BC"],
    "4": ["S_IVA0", "P_IVA0_BC"]
}

class import_replacements(object):
    def __init__(self, dbname, user, passwd, products_file):
        """método incial"""

        try:
            self.url_template = "http://%s:%s/xmlrpc/%s"
            self.server = "localhost"
            self.port = 8069
            self.dbname = dbname
            self.user_name = user
            self.user_passwd = passwd
            self.products_file = products_file

            #
            # Conectamos con OpenERP
            #
            login_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'common'))
            self.user_id = login_facade.login(self.dbname, self.user_name, self.user_passwd)
            self.object_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'object'))

            res = self.import_replacements()
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

    def getSupplierByRef(self, partner_ref):
        partner_ids = self.search("res.partner", [('supplier','=',True),('ref','=',partner_ref)])
        return partner_ids and partner_ids[0] or False

    def getTaxes(self, tax_name):
        tax_ids = self.search("account.tax", [('name', '=', tax_name)])
        return tax_ids

    def getUomByName(self, uom_name):
        uom_ids = self.search("product.uom", [('name', '=', uom_name)])
        return uom_ids and uom_ids[0] or False

    def getCategoryByName(self, categ_name):
        categ_ids = self.search("product.category", [('name', '=like', categ_name+u"%")])
        return categ_ids and categ_ids[-1] or False

    def getProductByCode(self, code): # Incluimos tb codigos desactivados
        product_ids = self.search("product.product", [('default_code', '=', code)])
        return product_ids  or False
        
    def getProductByCodeNoExact(self, code): # Incluimos tb codigos desactivados
        
        if len(code) <= 2 or code.strip() == "":
            print "CODIGO IGNORADO ", code
            return False
        else :
            product_ids = self.search("product.product", [('default_code', 'like', code+u"%"),
            '|', ('active', '=', True), ('active', '=', False)])
        return product_ids  or False




    def import_replacements(self):
        pwb = xlrd.open_workbook(self.products_file, encoding_override="utf-8")
        sh = pwb.sheet_by_index(0)
        cont = 1
        all_lines = sh.nrows - 1
        print "products no: ", all_lines
        lista_no_encontrados = []
        lista_encontrados = []
        for rownum in range(1, all_lines):
            record = sh.row_values(rownum)
            try:
                if str(record[1]).strip() <> "":
                    product_ids = self.getProductByCodeNoExact(str(record[1]))
                else:
                    product_ids = False
                if product_ids:
                    print "REPUESTOS para Bomba: ", str(record[1])
                    print "Para bombas", product_ids
                    if str(record[1]) not in lista_encontrados:
                         lista_encontrados.append(str(record[1]))
                    replace_ids = self.getProductByCode(str(record[3]))
                    if not replace_ids:
                        print "Repuesto no encontrado en BD: ", str(record[3])
                    else:
                        for repuesto_id in replace_ids:
                            print "Añadiendo Repuesto : ", str(record[3])
                            replace_vals = {
                                'product_id': repuesto_id,
                                'qty': int(record[6]),
                                'disassembly_ref':  str(record[4]),
                                'replacement_for_ids': [(6, False, product_ids)]
                            }
                            print replace_vals
                            repl_id = self.create('product.replacement', replace_vals)
                            #self.write('product.replacement', repl_id,
                            #           {'replacement_for_ids': (4, product_ids, False)})
                else:
                     print "Bomba no encontrada en BD: ", str(record[1])
                     #print str(record[1])
                     if str(record[1]) not in lista_no_encontrados:
                         lista_no_encontrados.append(str(record[1]))
                print "%s de %s" % (cont, all_lines)
                cont += 1
            except Exception, e:
                print "EXCEPTION: REC: ", (record, e)
        print "NO ENCONTRADOS"
        print lista_no_encontrados
        print "ENCONTRADOS"
        print lista_encontrados



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print u"Uso: %s <dbname> <user> <password> <products.xls>" % sys.argv[0]
    else:
        import_replacements(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
