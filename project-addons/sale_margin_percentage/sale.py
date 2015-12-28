# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Pexego Sistemas Informáticos All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@pexego.es>$
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

from openerp.osv import fields, orm


class sale_order(orm.Model):

    _inherit = "sale.order"

    def _product_margin_perc(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for sale in self.browse(cr, uid, ids, context=context):
            result[sale.id] = 0.0
            if sale.amount_untaxed != 0:
                for line in sale.order_line:
                    result[sale.id] += line.margin or 0.0
                result[sale.id] = round((result[sale.id] * 100) /
                                    sale.amount_untaxed, 2)
        return result

    def _get_total_price_purchase(self, cr, uid, ids, field_name, arg,
                                  context=None):
        result = {}
        for sale in self.browse(cr, uid, ids, context=context):
            result[sale.id] = 0.0
            for line in sale.order_line:
                if line.product_id:
                    if line.purchase_price:
                        result[sale.id] += line.purchase_price * \
                            line.product_uos_qty
                    else:
                        result[sale.id] += line.product_id.standard_price * \
                            line.product_uos_qty
        return result

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        sale_obj = self.pool.get('sale.order.line')
        for line in sale_obj.browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns = {
        'total_purchase': fields.function(_get_total_price_purchase,
                                          string='Price purchase',
                                          store={
                                              'sale.order.line': (_get_order,
                                                                  ['margin'],
                                                                  20),
                                              'sale.order': (lambda self, cr,
                                                             uid, ids, c={}:
                                                             ids,
                                                             ['order_line'],
                                                             20),
                                          }),
        'margin_perc': fields.function(_product_margin_perc, string='Margin %',
                                  help="It gives profitability by calculating \
                                        percentage.",
                                  store={
                                      'sale.order.line':
                                          (_get_order, ['margin'], 20),
                                      'sale.order':
                                          (lambda self, cr, uid, ids, c={}:
                                           ids, ['order_line'], 20),
                                  }),
    }


from openerp import models, fields, api


class sale_order_line(models.Model):

    _inherit = "sale.order.line"

    @api.one
    def _get_cost_price(self):
        cost_price = 0.0
        if self.pack_child_line_ids:
            child_lines = self.pack_child_line_ids
            cost_price = sum(child_lines.with_context(for_parent=True)._get_cost_price())
        elif self._context.get('for_parent', False):
            if self.purchase_price and self.product_uos_qty:
                cost_price = self.purchase_price * self.product_uos_qty
            elif self.product_id.standard_price:
                cost_price = self.product_id.standard_price * self.product_uos_qty
        elif not self.pack_parent_line_id:
            if self.purchase_price and self.product_uos_qty:
                cost_price = self.purchase_price
            elif self.product_id.standard_price:
                cost_price = self.product_id.standard_price
        return cost_price

    @api.one
    @api.depends('product_id', 'price_unit', 'product_uos_qty', 'purchase_price', 'discount',
                 'pack_child_line_ids', 'pack_parent_line_id')
    def _product_margin(self):
        margin = 0.0
        if self.product_id:
            cost_price = self._get_cost_price()[0]
        else:
            cost_price = self.purchase_price
        if cost_price:
            margin = round((self.price_unit * self.product_uos_qty *
                           (100.0 - self.discount) / 100.0) -
                           (cost_price * self.product_uos_qty), 2)
            self.margin_perc = round((margin * 100) /
                                                (cost_price * self.product_uos_qty), 2)
        self.margin = margin

    margin = fields.Float('Margin', compute='_product_margin', store=True)
    margin_perc = fields.Float('Margin', compute='_product_margin', store=True)
