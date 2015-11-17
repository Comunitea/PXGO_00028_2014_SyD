# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import math
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp


class product_pack(orm.Model):
    _name = 'product.pack.line'
    _rec_name = 'product_id'
    _columns = {
        'parent_product_id': fields.many2one(
            'product.product', 'Parent Product',
            ondelete='cascade', required=True
        ),
        'quantity': fields.float('Quantity', required=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True
        ),
    }


class product_product(orm.Model):
    _inherit = 'product.product'

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            stock = super(product_product, self)._product_available(
                cr, uid, [product.id], field_names, arg, context)

            if not product.stock_depends:
                res[product.id] = stock[product.id]
                continue

            first_subproduct = True
            pack_stock = 0

            # Check if product stock depends on it's subproducts stock.
            if product.pack_line_ids:
                """ Go over all subproducts, take quantity needed for the pack
                and its available stock """
                for subproduct in product.pack_line_ids:

                    # if subproduct is a service don't calculate the stock
                    if subproduct.product_id.type == 'service':
                        continue
                    if first_subproduct:
                        subproduct_quantity = subproduct.quantity
                        subproduct_stock = self._product_available(cr, uid, [subproduct.product_id.id], field_names, arg, context)[subproduct.product_id.id]['qty_available']
                        if subproduct_quantity == 0:
                            continue

                        """ Calculate real stock for current pack from the
                        subproduct stock and needed quantity """
                        pack_stock = math.floor(
                            subproduct_stock / subproduct_quantity)
                        first_subproduct = False
                        continue

                    # Take the info of the next subproduct
                    subproduct_quantity_next = subproduct.quantity
                    subproduct_stock_next = self._product_available(cr, uid, [subproduct.product_id.id], field_names, arg, context)[subproduct.product_id.id]['qty_available']

                    if (
                        subproduct_quantity_next == 0
                        or subproduct_quantity_next == 0.0
                    ):
                        continue

                    pack_stock_next = math.floor(
                        subproduct_stock_next / subproduct_quantity_next)

                    # compare the stock of a subproduct and the next subproduct
                    if pack_stock_next < pack_stock:
                        pack_stock = pack_stock_next

                # result is the minimum stock of all subproducts
                res[product.id] = {
                    'qty_available': pack_stock,
                    'incoming_qty': 0,
                    'outgoing_qty': 0,
                    'virtual_available': pack_stock,
                }
            else:
                res[product.id] = stock[product.id]
        return res

    def _search_product_quantity(self, cr, uid, obj, name, domain, context):
        return super(product_product, self)._search_product_quantity(cr, uid, obj, name, domain, context)

    _columns = {
        'stock_depends': fields.boolean(
            'Stock depends of components',
            help='Mark if pack stock is calcualted from component stock'
        ),
        'pack_fixed_price': fields.boolean(
            'Pack has fixed price',
            help="""
            Mark this field if the public price of the pack should be fixed.
            Do not mark it if the price should be calculated from the sum of
            the prices of the products in the pack.
        """
        ),
        'pack_line_ids': fields.one2many(
            'product.pack.line', 'parent_product_id', 'Pack Products',
            help='List of products that are part of this pack.'
        ),
        'qty_available': fields.function(_product_available, multi='qty_available',
            type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Quantity On Hand',
            fnct_search=_search_product_quantity,
            help="Current quantity of products.\n"
                 "In a context with a single Stock Location, this includes "
                 "goods stored at this Location, or any of its children.\n"
                 "In a context with a single Warehouse, this includes "
                 "goods stored in the Stock Location of this Warehouse, or any "
                 "of its children.\n"
                 "stored in the Stock Location of the Warehouse of this Shop, "
                 "or any of its children.\n"
                 "Otherwise, this includes goods stored in any Stock Location "
                 "with 'internal' type."),
        'virtual_available': fields.function(_product_available, multi='qty_available',
            type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Forecast Quantity',
            fnct_search=_search_product_quantity,
            help="Forecast quantity (computed as Quantity On Hand "
                 "- Outgoing + Incoming)\n"
                 "In a context with a single Stock Location, this includes "
                 "goods stored in this location, or any of its children.\n"
                 "In a context with a single Warehouse, this includes "
                 "goods stored in the Stock Location of this Warehouse, or any "
                 "of its children.\n"
                 "Otherwise, this includes goods stored in any Stock Location "
                 "with 'internal' type."),
        'incoming_qty': fields.function(_product_available, multi='qty_available',
            type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Incoming',
            fnct_search=_search_product_quantity,
            help="Quantity of products that are planned to arrive.\n"
                 "In a context with a single Stock Location, this includes "
                 "goods arriving to this Location, or any of its children.\n"
                 "In a context with a single Warehouse, this includes "
                 "goods arriving to the Stock Location of this Warehouse, or "
                 "any of its children.\n"
                 "Otherwise, this includes goods arriving to any Stock "
                 "Location with 'internal' type."),
        'outgoing_qty': fields.function(_product_available, multi='qty_available',
            type='float', digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Outgoing',
            fnct_search=_search_product_quantity,
            help="Quantity of products that are planned to leave.\n"
                 "In a context with a single Stock Location, this includes "
                 "goods leaving this Location, or any of its children.\n"
                 "In a context with a single Warehouse, this includes "
                 "goods leaving the Stock Location of this Warehouse, or "
                 "any of its children.\n"
                 "Otherwise, this includes goods leaving any Stock "
                 "Location with 'internal' type."),
    }

    _defaults = {
        'pack_fixed_price': True,
    }
