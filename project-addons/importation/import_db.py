# -*- coding: utf-8 -*-
from com.ziclix.python.sql import zxJDBC
import sys
import xmlrpclib
import socket
import traceback
import re
import base64

UOM_MAP = {
    'KG': 'kg',
    'L': 'Liter(s)',
    'M': 'm',
    'UD': 'Unit(s)'
}

UOM_CATEG_MAP = {
    'KG': 'Weight',
    'L': 'Volume',
    'M': 'Length / Distance',
    'UD': 'Unit'
}

CATEG_MAP = {
    '00': "BOMBAS AZCUE",
    '01': "REPUESTOS BOMBAS AZCUE",
    '02': "REPUESTOS DE MOTORES (a extinguir)",
    '03': "COMPRESORES ABC",
    '04': "TRATAMIENTO DE AGUAS",
    '05': "SEGMENTOS BAR-VIZ (a extinguir)",
    '06': "OTRA MAQUINARIA INDUSTRIAL",
    '07': "BOMBAS DE IMPULSOR FLEXIBLE",
    '08': "RODAMIENTOS Y RETENES (a extinguir)",
    '09': "BOMBAS SACI",
    '10': "ACOPLAMIENTOS (a extinguir)",
    '11': "INSTALACIONES Y SERVICIOS",
    '12': "DEPURADORAS AGUAS RESIDUALES URBANAS"
}

ESCAPE_STATES_MAP = ["00651","8961","8962","90059","91860","92155"]

class SyDImport:
    """
    Importa a OpenERP datos de una base de datos SqlServer para Calor Color.
    """

    def __init__(self, dbname, user, passwd):
        """
        Inicializar las opciones por defecto y conectar con OpenERP
        """


    #-------------------------------------------------------------------------
    #--- WRAPPER XMLRPC OPENERP ----------------------------------------------
    #-------------------------------------------------------------------------


        self.url_template = "http://%s:%s/xmlrpc/%s"
        self.server = "localhost"
        self.port = 8069
        self.dbname = dbname
        self.user_name = user
        self.user_passwd = passwd
        self.user_id = 0

        #
        # Conectamos con OpenERP
        #
        login_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'common'))
        self.user_id = login_facade.login(self.dbname, self.user_name, self.user_passwd)
        self.object_facade = xmlrpclib.ServerProxy(self.url_template % (self.server, self.port, 'object'))

        #
        # Fichero Log de Excepciones
        #
        self.file = open("importation_log.txt", "w")

    def exception_handler(self, exception):
        """Manejador de Excepciones"""
        print "HANDLER: ", (exception)
        self.file.write("WARNING: %s\n\n\n" % repr(exception))
        return True

    def create(self, model, data, context={}):
        """
        Wrapper del método create.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                model, 'create', data, context)

            if isinstance(res, list):
                res = res[0]

            return res
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en create: %s' % (err.faultCode, err.faultString))

    def exec_workflow(self, model, signal, ids):
        """ejecuta un workflow por xml rpc"""
        try:
            res = self.object_facade.exec_workflow(self.dbname, self.user_id, self.user_passwd, model, signal, ids)
            return res
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en exec_workflow: %s' % (err.faultCode, err.faultString))

    def search(self, model, query, context={}):
        """
        Wrapper del método search.
        """
        try:
            ids = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                model, 'search', query, context)
            return ids
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en search: %s' % (err.faultCode, err.faultString))


    def read(self, model, ids, fields, context={}):
        """
        Wrapper del método read.
        """
        try:
            data = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                    model, 'read', ids, fields, context)
            return data
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en read: %s' % (err.faultCode, err.faultString))


    def write(self, model, ids, field_values, context={}):
        """
        Wrapper del método write.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                    model, 'write', ids, field_values, context)
            return res
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en write: %s' % (err.faultCode, err.faultString))


    def unlink(self, model, ids, context={}):
        """
        Wrapper del método unlink.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                    model, 'unlink', ids, context)
            return res
        except socket.error, err:
            raise Exception(u'Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception(u'Error %s en unlink: %s' % (err.faultCode, err.faultString))

    def default_get(self, model, fields_list=[], context={}):
        """
        Wrapper del método default_get.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                    model, 'default_get', fields_list, context)
            return res
        except socket.error, err:
            raise Exception('Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception('Error %s en default_get: %s' % (err.faultCode, err.faultString))

    def execute(self, model, method, ids, context={}):
        """
        Wrapper del método execute.
        """
        try:
            res = self.object_facade.execute(self.dbname, self.user_id, self.user_passwd,
                                    model, method, ids, context)
            return res
        except socket.error, err:
            raise Exception('Conexión rechazada: %s!' % err)
        except xmlrpclib.Fault, err:
            raise Exception('Error %s en execute: %s' % (err.faultCode, err.faultString))

    def _get_uom_id(self, code):
        """obtiene el id de la unidad de medidad desde su código, sino la encontrara se crea"""
        if code:
            uom_id = self.search('product.uom', [('name', '=', UOM_MAP[code])])
            if uom_id:
                return uom_id[0]
            else:
                categ_id = self.search('product.uom.categ', [('name', '=', UOM_CATEG_MAP[code])])
                if not categ_id:
                    categ_id = self.create('product.uom.categ', {'name': UOM_CATEG_MAP[code]})
                else:
                    categ_id = categ_id[0]

                uom_id = self.create('product.uom', {
                                                    'active': True,
                                                    'category_id': categ_id,
                                                    'name': UOM_MAP[code]
                                                })
                return uom_id

        return False

    def _get_country_id_by_code(self, code, allow_nulls = True):
        """Obtiene el id de res.country desde un códico del país"""
        if code:
            country_ids =  self.search(u'res.country', [('code', '=', code)])
            if len(country_ids) > 1:
                raise Exception(u'Error, se encontraron más de un país relacionado con el código de país: %s' % code)
            elif not country_ids:
                if not allow_nulls:
                    raise Exception(u'Error, no se ha encontrado ningún pí­s relacionado con el código de país: %s' % code)
                else:
                    return False
            return country_ids[0]
        else:
            return False

    def _get_state_id_by_code(self, code, country_id, allow_nulls = True):
        """Obtiene el id de res.country.state desde un código de provincia y de país"""
        state_ids =  self.search(u'res.country.state', [('code', '=', code), ('country_id', '=', country_id)])
        if len(state_ids) > 1:
            raise Exception(u'Error, se ha encontrado más de una provincia relacionada con el código de provincia: %s' % code)
        elif not state_ids:
            if not allow_nulls:
                raise Exception(u'Error, no se ha encontrado ninguna provincia relacionada con el código de provincia: %s' % code)
            else:
                return False
        return state_ids[0]

    def _get_product_category(self, name):
        """buscasmo una categoría de producto por su nombre"""
        categ_ids = self.search('product.category', [('name', '=', name)])
        return categ_ids and categ_ids[0] or False

    def _get_default_category(self, category_name):
        """obtiene la categoría pedida sino la encunetra la crea"""
        category_ids = self.search('product.category', [('name', '=', category_name)])
        if category_ids:
            return category_ids[0]
        else:
            return self.create('product.category', {
                                'name': category_name
                        })
    def _get_bank_by_code(self, code):
        """obtiene eun banco en Openerp por el código"""
        bank_ids = self.search('res.bank', [('code', '=', code)])
        return bank_ids and bank_ids[0] or False

    def get_partner_vat(self, cif_nif, country_code=False):
        """
        Obtiene el vat (NIF/CIF),
        lo limpia (eliminamos espacios y otros símbolos),
        y hace una comprobación ligera de que sea válido.
        """
        cif_nif = (cif_nif and cif_nif.strip(" ") != "") and cif_nif.upper().replace("-","").replace(" ","").replace(".","") or False

        if cif_nif and country_code and (re.match(r'[A-Z][0-9]{7}[A-Z0-9]', cif_nif) or re.match(r'[0-9]{8}[A-Z]', cif_nif)):
            return country_code + cif_nif
        elif cif_nif and (re.match(r'[A-Z]{2}[A-Z][0-9]{7}[A-Z0-9]', cif_nif) or re.match(r'[A-Z]{2}[0-9]{8}[A-Z]', cif_nif)):
            return cif_nif
        else:
            return False

    def _get_supplier_by_name(self, partner_name):
        """Obtiene un proveedor por nombre"""
        suppliers = self.search('res.partner', [('supplier', '=', True),('name', '=', partner_name.strip(' ')),('active', 'in', [True,False])])
        return suppliers and suppliers[0] or False

    def import_country_states(self, cr):
        """Importamos provincias nuevas"""
        cr.execute("select count(*) as count from Z_SYSTEM_PC_PROVINCIAS where xnombre not like 'Desconocid%'")
        row_count = cr.fetchone()
        print "Número de provincias: ", (row_count[0])
        num_rows = row_count[0]

        #nos traemos todos los registros
        cr.execute("""select Z_SYSTEM_PC_PROVINCIAS.XNOMBRE, Z_SYSTEM_PC_PAISES.XPAIS_ID, XCODIGO_ISOA, XPROVINCIA_ID
                    from Z_SYSTEM_PC_PROVINCIAS
                    inner join Z_SYSTEM_PC_PAISES
                    on Z_SYSTEM_PC_PROVINCIAS.XPAIS_ID = Z_SYSTEM_PC_PAISES.XPAIS_ID
                    where Z_SYSTEM_PC_PROVINCIAS.XNOMBRE not like 'Desconocid%'""")
        rows = cr.fetchall()

        #recorremos los registros
        imported_rows = 0
        for row in rows:
            try:
                if str(row[1]) + str(row[3]) not in ESCAPE_STATES_MAP and row[2] != 'ES':
                    state_vals = {
                        'code': str(row[3]),
                        'country_id': self._get_country_id_by_code(row[2], False),
                        'name': row[0].strip(' ')
                    }

                    state_ids = self.search(u"res.country.state", [('name', '=', state_vals['name'])])
                    if not state_ids:
                        self.create(u"res.country.state", state_vals)

                imported_rows += 1
                print "%s de %s" % (imported_rows, num_rows)
            except Exception, ex:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,limit=2, file=sys.stdout)
                self.exception_handler(u"Error importando PROVINCIAS: %s en Access %s" % (repr(ex), repr(row)))

        print "Procesados %s de %s registros en PROVINCIAS." % (imported_rows, num_rows)
        return str(imported_rows) + " de " + str(num_rows)

    def import_partner_bank_accounts(self, cr, partner_id, db_id, model):
        """importamos las cuentas bancarias de las empresas"""
        if model == 'supplier':
            cr.execute("""select XCOD_BANCO, XCOD_IBAN, XCOD_OFICINA, XCTA_BANCO, XDIGITOS_CONTR,
                          Z_SYSTEM_PF_CUENTAS_LOC.XNOMBRE, XCODIGO_ISOA, XNOM_BANCO, XNOM_OFICINA
                       from Z_SYSTEM_PC_PROVEEDORES
                       inner join Z_SYSTEM_PF_CUENTAS_LOC
                       on XPROVEEDOR_ID = XCUENTA_ID
                       left join Z_SYSTEM_PC_PAISES
                       on Z_SYSTEM_PF_CUENTAS_LOC.XPAIS_ID = Z_SYSTEM_PC_PAISES.XPAIS_ID
                       where (XCOD_BANCO is not null or XCOD_IBAN is not null) and XPLAN_ID in ('PRO','ACR') and XPROVEEDOR_ID = ?""", (db_id,))
        else:
            cr.execute("""select XCOD_BANCO, XCOD_IBAN, XCOD_OFICINA, XCTA_BANCO, XDIGITOS_CONTR,
                          Z_SYSTEM_PF_CUENTAS_LOC.XNOMBRE, XCODIGO_ISOA, XNOM_BANCO, XNOM_OFICINA
                       from Z_SYSTEM_PC_CLIENTES
                       inner join Z_SYSTEM_PF_CUENTAS_LOC
                       on XCLIENTE_ID = XCUENTA_ID
                       left join Z_SYSTEM_PC_PAISES
                       on Z_SYSTEM_PF_CUENTAS_LOC.XPAIS_ID = Z_SYSTEM_PC_PAISES.XPAIS_ID
                       where (XCOD_BANCO is not null or XCOD_IBAN is not null) and XPLAN_ID = 'CLI' and XCLIENTE_ID = ?""", (db_id,))
        rows = cr.fetchall()

        for row in rows:
            if row[0] and row[2] and row[4] and row[3]:
                ccc = row[0]  + " " + row[2] + " " + row[4] + " " + row[3]
            else:
                ccc = False
            if ccc or row[1]:
                bank_values = {
                        'state': ccc and 'bank' or 'iban',
                        'acc_number': ccc or row[1],
                        'sequence': 0,
                        'partner_id': partner_id,
                        'country_id': self._get_country_id_by_code(row[6], True),
                        'bank': row[0] and self._get_bank_by_code(row[0]) or False,
                        'bank_name': row[7] or "",
                        'owner_name': row[5] or "",
                        'street': row[8] or "",
                    }

                bank_ids = self.search(u"res.partner.bank", [('partner_id', '=', bank_values['partner_id']), ('acc_number', '=', bank_values['acc_number'])])
                if bank_ids:
                    #Actualizar
                    self.write(u"res.partner.bank", [bank_ids[0]], bank_values)
                else:
                    self.create(u"res.partner.bank", bank_values)
        return True

    def import_send_addresses(self, cr, partner_id, db_id):
        """importamos el resto de direcciones de envío de un cliente"""
        cr.execute("""select XFAX, XCOD_POSTAL, XDOMICILIO, XEMAIL, Z_SYSTEM_PL_CLI_ENV.XNOMBRE, XCODIGO_ISOA, XPOBLACION, XPROVINCIA_ID, XTELEFONO
                        from Z_SYSTEM_PL_CLI_ENV
                        left join Z_SYSTEM_PC_PAISES on Z_SYSTEM_PL_CLI_ENV.XPAIS_ID = Z_SYSTEM_PC_PAISES.XPAIS_ID
                        where XEMPRESA_ID = 'SYD' and XCLIENTE_ID = ?""", (db_id,))

        rows = cr.fetchall()

        for row in rows:
            if row[2]:
                address_vals = {
                    'name': row[4] and row[4].strip(' ') or "",
                    'type': 'delivery',
                    'state_id': (row[7] and row[5]) and self._get_state_id_by_code(row[7], self._get_country_id_by_code(row[5], True), allow_nulls = True) or False,
                    'phone': row[8] and row[8].strip(' ') or "",
                    'zip': row[1] and row[1].strip(' ') or "",
                    'country_id': self._get_country_id_by_code(row[5], True),
                    'parent_id': partner_id,
                    'street': row[2] and row[2].strip(' ') or "",
                    'city': row[6] and row[6].strip(' ') or "",
                    'fax': row[0] and row[0].strip(' ') or "",
                    'active': True,
                    'customer': False,
                    'email': row[3] and row[3].strip(' ') or ""
                }

                address_default_ids = self.search(u"res.partner", [('parent_id', '=', address_vals['parent_id']), ('type', '=', address_vals['type']), ('name', '=', address_vals['name'])])
                if address_default_ids:
                    #Actualizar
                    self.write(u"res.partner", [address_default_ids[0]], address_vals)
                else:
                    self.create(u"res.partner", address_vals)

        return True

    def import_invoice_addresses(self, cr, partner_id, db_id):
        """importamos el resto de direcciones de facturación de un cliente"""
        cr.execute("""select XFAX, XCOD_POSTAL, XDOMICILIO, XEMAIL, Z_SYSTEM_PL_CLI_FACT.XNOMBRE, XCODIGO_ISOA, XPOBLACION, XPROVINCIA_ID, XTELEFONO
                        from Z_SYSTEM_PL_CLI_FACT
                        left join Z_SYSTEM_PC_PAISES on Z_SYSTEM_PL_CLI_FACT.XPAIS_ID = Z_SYSTEM_PC_PAISES.XPAIS_ID
                        where XEMPRESA_ID = 'SYD' and XCLIENTE_ID = ?""", (db_id,))

        rows = cr.fetchall()

        for row in rows:
            if row[2]:
                address_vals = {
                    'name': row[4] and row[4].strip(' ') or "",
                    'type': 'invoice',
                    'state_id': (row[7] and row[5]) and self._get_state_id_by_code(row[7], self._get_country_id_by_code(row[5], True), allow_nulls = True) or False,
                    'phone': row[8] and row[8].strip(' ') or "",
                    'zip': row[1] and row[1].strip(' ') or "",
                    'country_id': self._get_country_id_by_code(row[5], True),
                    'parent_id': partner_id,
                    'street': row[2] and row[2].strip(' ') or "",
                    'city': row[6] and row[6].strip(' ') or "",
                    'fax': row[0] and row[0].strip(' ') or "",
                    'active': True,
                    'customer': False,
                    'email': row[3] and row[3].strip(' ') or ""
                }

                address_default_ids = self.search(u"res.partner", [('parent_id', '=', address_vals['parent_id']), ('type', '=', address_vals['type']), ('name', '=', address_vals['name'])])
                if address_default_ids:
                    #Actualizar
                    self.write(u"res.partner", [address_default_ids[0]], address_vals)
                else:
                    self.create(u"res.partner", address_vals)

        return True

    def import_customers(self, cr):
        """Importamos clientes"""
        cr.execute("""select count(*) as count from Z_SYSTEM_PC_CLIENTES
                    where XEMPGEN_ID = 'SYD'""")
        row_count = cr.fetchone()
        print "Número de clientes: ", (row_count[0])
        num_rows = row_count[0]

        #nos traemos todos los registros
        cr.execute("""select min(Z_SYSTEM_PC_CLIENTES.XCLIENTE_ID), min(Z_SYSTEM_PC_CLIENTES.XCOD_POSTAL),
                    min(Z_SYSTEM_PC_CLIENTES.XDOMICILIO), min(Z_SYSTEM_PC_CLIENTES.XNIF),
                    min(XNIF_UE), min(Z_SYSTEM_PC_CLIENTES.XNOMABREV), min(Z_SYSTEM_PC_CLIENTES.XNOMBRE),
                    min(Z_SYSTEM_PC_CLIENTES.XPOBLACION), min(Z_SYSTEM_PC_CLIENTES.XPROVINCIA_ID), min(Z_SYSTEM_PC_PAISES.XCODIGO_ISOA),
                    min(Z_SYSTEM_PL_CLI_COB.XFPAGO_ID), min(Z_SYSTEM_PL_CLI_COB.XEMAIL), min(Z_SYSTEM_PL_CLI_COB.XFAX), min(Z_SYSTEM_PL_CLI_COB.XTELEFONO),
                    from Z_SYSTEM_PC_CLIENTES
                    left join Z_SYSTEM_PL_CLI_COB on Z_SYSTEM_PC_CLIENTES.XCLIENTE_ID = Z_SYSTEM_PL_CLI_COB.XCLIENTE_ID
                    left join Z_SYSTEM_PC_PAISES on Z_SYSTEM_PC_CLIENTES.XPAIS_ID = Z_SYSTEM_PC_PAISES.XPAIS_ID
                    where Z_SYSTEM_PC_CLIENTES.XEMPGEN_ID = 'SYD'
                    group by Z_SYSTEM_PC_CLIENTES.XCLIENTE_ID""")
        rows = cr.fetchall()

        #recorremos los registros
        imported_rows = 0
        for row in rows:
            try:
                if row[6]:
                    partner_vals = {
                        'name': row[6],
                        'active': True,
                        'lang': 'es_ES',
                        'customer': True,
                        'ref': row[0] or "",
                        'comercial': row[5] and row[5].strip(' ') or "",
                        'state_id': (row[8] and row[9]) and self._get_state_id_by_code(row[8], self._get_country_id_by_code(row[9], True), allow_nulls = True) or False,
                        'phone': row[13] and row[13].strip(' ') or "",
                        'zip': row[1] or "",
                        'country_id': self._get_country_id_by_code(row[9], True),
                        'street': row[2] and row[2].strip(' ') or "",
                        'city': row[7] and row[7].strip(' ') or "",
                        'fax': row[12] and row[12].strip(' ') or "",
                        'active': True,
                        'type': 'default',
                        'is_company': True,
                        'email': row[11] and row[11].strip(' ') or ""
                    }

                    partner_ids = self.search(u'res.partner', [('name', '=', partner_vals['name']), ('active', 'in', [True,False]), ('customer', '=', True)])
                    partner_id = False
                    if not partner_ids:
                        partner_id = self.create(u"res.partner", partner_vals)
                    else:
                        self.write("res.partner", [partner_ids[0]], partner_vals)
                        partner_id = partner_ids[0]

                    #Intentamos escribir el nif
                    if row[3] or row[4]:
                        try:
                            self.write("res.partner", [partner_id], {'vat': (row[3] or row[4]) and (self.get_partner_vat((row[4] or row[3]), row[9] or 'ES') or (row[4] or row[3])) or False})
                        except:
                            print "El nif_ue %s falló" % (row[3] or row[4]) and self.get_partner_vat((row[4] or row[3]), row[9] or 'ES') or (row[4] or row[3])
                            try:
                                self.write("res.partner", [partner_id], {'vat': (row[3] or row[4]) and (self.get_partner_vat((row[3] or row[4]), row[9] or 'ES') or (row[3] or row[4])) or False})
                            except:
                                print "El nif %s falló" % (row[3] or row[4]) and (self.get_partner_vat((row[3] or row[4]), row[9] or 'ES') or (row[3] or row[4])) or False

                    self.import_partner_bank_accounts(cr, partner_id, row[0], 'customer')
                    self.import_send_addresses(cr, partner_id, row[0])
                    self.import_invoice_addresses(cr, partner_id, row[0])

                imported_rows += 1
                print "%s de %s" % (imported_rows, num_rows)
            except Exception, ex:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,limit=2, file=sys.stdout)
                self.exception_handler(u"Error importando CLIENTES: %s en Access %s" % (repr(ex), repr(row)))

        print "Procesados %s de %s registros en CLIENTES." % (imported_rows, num_rows)
        return str(imported_rows) + " de " + str(num_rows)

    def import_suppliers(self, cr):
        """Importamos proveedores"""
        cr.execute("""select count(*) as count from Z_SYSTEM_PC_PROVEEDORES
                    where XEMPGEN_ID = 'SYD'""")
        row_count = cr.fetchone()
        print "Número de proveedores: ", (row_count[0])
        num_rows = row_count[0]

        #nos traemos todos los registros
        cr.execute("""select min(Z_SYSTEM_PC_PROVEEDORES.XPROVEEDOR_ID), min(Z_SYSTEM_PC_PROVEEDORES.XPROVINCIA_ID), min(Z_SYSTEM_PC_PROVEEDORES.XCOD_POSTAL),
                                min(Z_SYSTEM_PC_PROVEEDORES.XDOMICILIO), min(XNIF), min(XNIF_UE), min(XNOMABREV), min(Z_SYSTEM_PC_PROVEEDORES.XNOMBRE),
                                min(Z_SYSTEM_PC_PROVEEDORES.XPAIS_ID), min(XCODIGO_ISOA), min(Z_SYSTEM_PC_PROVEEDORES.XPOBLACION), min(XTELEFONO), min(XEMAIL), min(XFAX)
                        from Z_SYSTEM_PC_PROVEEDORES
                        left join Z_SYSTEM_PF_CUENTAS_LOC on Z_SYSTEM_PF_CUENTAS_LOC.XCUENTA_ID = Z_SYSTEM_PC_PROVEEDORES.XPROVEEDOR_ID and XPLAN_ID in ('PRO','ACR')
                        left join Z_SYSTEM_PC_PAISES on Z_SYSTEM_PC_PROVEEDORES.XPAIS_ID = Z_SYSTEM_PC_PAISES.XPAIS_ID
                        where Z_SYSTEM_PC_PROVEEDORES.XEMPGEN_ID = 'SYD'
                        group by Z_SYSTEM_PC_PROVEEDORES.XPROVEEDOR_ID""")
        rows = cr.fetchall()

        #recorremos los registros
        imported_rows = 0
        for row in rows:
            try:
                if row[7]:
                    partner_vals = {
                        'name': row[7].strip(' '),
                        'active': True,
                        'lang': 'es_ES',
                        'customer': False,
                        'supplier': True,
                        'ref': row[0] or "",
                        'comercial': row[6] and row[6].strip(' ') or "",
                        'state_id': (row[1] and row[9]) and self._get_state_id_by_code(row[1], self._get_country_id_by_code(row[9], True), allow_nulls = True) or False,
                        'phone': row[11] and row[11].strip(' ') or "",
                        'zip': row[2] or "",
                        'country_id': self._get_country_id_by_code(row[9], True),
                        'street': row[3] and row[3].strip(' ') or "",
                        'city': row[10] and row[10].strip(' ') or "",
                        'fax': row[13] and row[13].strip(' ') or "",
                        'type': 'default',
                        'is_company': True,
                        'email': row[12] and row[12].strip(' ') or ""
                    }

                    partner_ids = self.search(u'res.partner', [('name', '=', partner_vals['name']), ('active', 'in', [True,False]), ('supplier', '=', True)])
                    partner_id = False
                    if not partner_ids:
                        partner_id = self.create(u"res.partner", partner_vals)
                    else:
                        self.write("res.partner", [partner_ids[0]], partner_vals)
                        partner_id = partner_ids[0]

                    #Intentamos escribir el nif
                    if row[4] or row[5]:
                        try:
                            self.write("res.partner", [partner_id], {'vat': (row[4] or row[5]) and (self.get_partner_vat((row[5] or row[4]), row[9] or 'ES') or (row[5] or row[4])) or False})
                        except:
                            print "El nif_ue %s falló" % (row[4] or row[5]) and self.get_partner_vat((row[5] or row[4]), row[9] or 'ES') or (row[5] or row[4])
                            try:
                                self.write("res.partner", [partner_id], {'vat': (row[4] or row[5]) and (self.get_partner_vat((row[4] or row[5]), row[9] or 'ES') or (row[4] or row[5])) or False})
                            except:
                                print "El nif %s falló" % (row[4] or row[5]) and (self.get_partner_vat((row[4] or row[5]), row[9] or 'ES') or (row[4] or row[5])) or False

                    self.import_partner_bank_accounts(cr, partner_id, row[0], 'supplier')

                imported_rows += 1
                print "%s de %s" % (imported_rows, num_rows)
            except Exception, ex:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,limit=2, file=sys.stdout)
                self.exception_handler(u"Error importando PROVEEDORES: %s en Access %s" % (repr(ex), repr(row)))

        print "Procesados %s de %s registros en PROVEEDORES." % (imported_rows, num_rows)
        return str(imported_rows) + " de " + str(num_rows)

    def create_product(self, cr, product_code, supply_method = 'buy', procure_method = 'make_to_stock'):
        """creamos o actualizamos un producto en Openerp recibiendo el código"""
        cr.execute("""select Z_SYSTEM_PL_ARTICULOS.XDESCRIPCION AS xdescripcion, Z_SYSTEM_PL_ARTECNICOS.XAFECTA_PMP AS xafecta_pmp, XGEST_EXIST AS xgest_exist, XGEST_LOTES AS xgest_lotes,
                        Z_SYSTEM_PL_ARTICULOS.XFAMILIA_ID AS xfamilia_id, XPREC_ESTANDAR AS xprec_estandar, XPREC_ULT_ENTRA AS xprec_ult_entra,
                        Z_SYSTEM_PL_ARTICULOS.XUNIDAD_PRIN_ID AS xunidad_prin_id, XOBSERVACIONES AS xobservaciones,
                        XPESO_BRUTO AS xpeso_bruto, XPESO_NETO AS xpeso_neto,
                        XCODALTER_ID AS xcodalter_id, Z_SYSTEM_PL_ARTICULOS.XARTICULO_ID AS xarticulo_id, XPREC_VENTA AS xprec_venta
                        from Z_SYSTEM_PL_ARTICULOS
                        left join Z_SYSTEM_PL_ARTECNICOS on  Z_SYSTEM_PL_ARTICULOS.XARTICULO_ID = Z_SYSTEM_PL_ARTECNICOS.XARTICULO_ID
                        left join Z_SYSTEM_PL_ARTALTER on Z_SYSTEM_PL_ARTICULOS.XARTICULO_ID = Z_SYSTEM_PL_ARTALTER.XARTICULO_ID
                        left join Z_SYSTEM_PL_ARTPREC on Z_SYSTEM_PL_ARTICULOS.XARTICULO_ID = Z_SYSTEM_PL_ARTPREC.XARTICULO_ID
                        where Z_SYSTEM_PL_ARTICULOS.xempresa_id = 'SYD' and Z_SYSTEM_PL_ARTICULOS.XARTICULO_ID = ?""", (product_code,))

        row = cr.fetchone()
        print "Inicio Creando Producto " + product_code
        product_id = False
        if row:
            product_vals = {
                'default_code': row[12].strip(' '),
                'active': True,
                'track_production': row[3] and True or False,
                'track_incoming': row[3] and True or False,
                'track_outgoing': row[3] and True or False,
                'procure_method': procure_method,
                'supply_method': supply_method,
                'standard_price': row[5] and float(row[5]) or 1.0,
                'list_price': row[13] and float(row[13]) or 1.0,
                'purchase_ok': row[6] and True or False,
                'uom_id': row[7] and self._get_uom_id(row[7].upper()) or 1,
                'sale_ok': row[13] and True or False,
                'name': row[0].strip(' '),
                'uom_po_id': row[7]  and self._get_uom_id(row[7].upper()) or 1,
                'type': row[2] and 'product' or 'consu',
                'description': row[8] and row[8].strip(' ') or False,
                'weight_net': row[10] and float(row[10]) or 0.0,
                'weight': row[9] and float(row[9]) or 0.0,
                'cost_method': row[1] and 'average' or 'standard',
                'categ_id': row[4] and self._get_product_category(CATEG_MAP[row[4]]) or self._get_default_category('SIN CATEGORIA'),
            }

            product_ids = self.search(u"product.product", [('default_code', '=', product_vals['default_code'])])
            if product_ids:
                print "Ya existente"
                self.write(u"product.product", [product_ids[0]], product_vals)
                product_id = product_ids[0]
            else:
                print "No existe, se crea"
                product_id = self.create(u"product.product", product_vals)

            print "Importado: ", product_vals['default_code']

        return product_id

    def import_product_suppliers(self, cr, product_id, product_code):
        """importamos los proveedores del producto"""
        cr.execute("""select XARTICULO_ID, XEMPRESA_ID, XDESC_LARGA, XDESCRIPCION_PROV, XPLAZO_ENTREGA, Z_SYSTEM_PC_PROVEEDORES.XPROVEEDOR_ID,
                        XREFERENCIA_PROV, Z_SYSTEM_PC_PROVEEDORES.XNOMBRE
                        from Z_SYSTEM_PL_ARTPROVEEDOR
                        inner join Z_SYSTEM_PC_PROVEEDORES
                        on Z_SYSTEM_PC_PROVEEDORES.XPROVEEDOR_ID = Z_SYSTEM_PL_ARTPROVEEDOR.XPROVEEDOR_ID
                        where XEMPRESA_ID = 'SYD' and XARTICULO_ID = ?""", (product_code,))
        rows = cr.fetchall()

        for row in rows:
            partner_id = self._get_supplier_by_name(row[7].strip(' '))
            if partner_id:
                supplier_info_vals = {
                    'product_tmpl_id': self.read('product.product', product_id, ['product_tmpl_id'])['product_tmpl_id'][0],
                    'delay': row[4] and int(row[4]) or 0,
                    'product_code': row[6] and row[6].strip(' ') or False,
                    'product_name': row[3] and row[3].strip(' ') or False,
                    'name': partner_id,
                    'observations': row[2] and row[2].strip(' ') or False,
                }
                sinfo_ids = self.search('product.supplierinfo', [('name', '=', supplier_info_vals['name']), ('product_tmpl_id', '=', supplier_info_vals['product_tmpl_id'])])
                if sinfo_ids:
                    self.write('product.supplierinfo', sinfo_ids, supplier_info_vals)
                else:
                    self.create('product.supplierinfo', supplier_info_vals)

        return True

    def import_products(self, cr):
        """Importamos los productos"""
        cr.execute("select count(*) as count from Z_SYSTEM_PL_ARTICULOS where xempresa_id = 'SYD'")
        row_count = cr.fetchone()
        print "Número de productos: ", (row_count[0])
        num_rows = row_count[0]

        #nos traemos todos los registros
        cr.execute("""select XARTICULO_ID
                        from Z_SYSTEM_PL_ARTICULOS
                        where XEMPRESA_ID = 'SYD'""")
        rows = cr.fetchall()

        #recorremos los registros
        imported_rows = 0

        for row in rows:
            try:
                product_id = self.create_product(cr, row[0])
                if product_id:
                    #importa los proveedores si los tuviera
                    self.import_product_suppliers(cr, product_id, row[0])

                imported_rows += 1
                print "%s de %s" % (imported_rows, num_rows)
            except Exception, ex:
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,limit=2, file=sys.stdout)
                self.exception_handler(u"Error importando PRODUCTOS: %s en Access %s" % (repr(ex), repr(row)))

        print "Procesados %s de %s registros en PRODUCTOS." % (imported_rows, num_rows)
        return str(imported_rows) + " de " + str(num_rows)

    def process_data(self):
        """
        Importa la bbdd
        """
        print "Intentamos establecer conexión"
        try:
            #
            # Nos conectamos a la bbdd de sql server
            #
            jdbc_url = "jdbc:ucanaccess:///home/likewise-open/PXGO/omar/Escritorio/ekon.accdb"
            username = ""
            password = ""
            driver = "net.ucanaccess.jdbc.UcanaccessDriver"
            conn = zxJDBC.connect(jdbc_url, username, password, driver)
            cr = conn.cursor()

            self.file.write("Iniciamos la Importación\n\n")
            print "Importando provincias"
            result = self.import_country_states(cr)
            print "Importando Clientes"
            result = self.import_customers(cr)
            print "Importando Proveedores"
            result = self.import_suppliers(cr)
            print "Importando Productos"
            result = self.import_products(cr)
            self.file.write("INFO: Importados PRODUCTOS, resultado: %s\n\n\n" % result)

            #cerramos el fichero
            cr.close()
            conn.close()
            self.file.close()
            return True

        except Exception, ex:
            print "Error al conectarse a las bbdd: ", (ex)
            sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print u"Uso: %s <dbname> <user> <password>" % sys.argv[0]
    else:
        ENGINE = SyDImport(sys.argv[1], sys.argv[2], sys.argv[3])

        ENGINE.process_data()
