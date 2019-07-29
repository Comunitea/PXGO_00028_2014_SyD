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

from odoo import models, fields, api


class sale_order(models.Model):

    _inherit = "sale.order"

    @api.depends('order_line.margin')
    @api.multi
    def _product_margin_perc(self):
        for sale in self:
            margin = 0.0
            if sale.amount_untaxed != 0:
                for line in sale.order_line:
                    margin += line.margin or 0.0
                sale.margin_perc = round((margin * 100) /
                                         sale.amount_untaxed, 2)

    @api.depends('order_line.margin')
    @api.multi
    def _get_total_price_purchase(self):
        for sale in self:
            total_purchase = 0.0
            for line in sale.order_line:
                if line.product_id:
                    if line.purchase_price:
                        total_purchase += line.purchase_price * \
                            line.product_uom_qty
                    else:
                        total_purchase += line.product_id.standard_price * \
                            line.product_uom_qty
            sale.total_purchase = total_purchase

    total_purchase = fields.Float(compute="_get_total_price_purchase",
                                  string='Price purchase', store=True)
    margin_perc = fields.Float(compute="_product_margin_perc",
                               string='Margin %',
                               help="It gives profitability by calculating "
                                    "percentage.", store=True)


class sale_order_line(models.Model):

    _inherit = "sale.order.line"

    @api.one
    def _get_cost_price(self):
        cost_price = self.product_id.standard_price
        #TODO: Migrar
        # ~ if self.pack_child_line_ids:
            # ~ child_lines = self.pack_child_line_ids
            # ~ cost_price = sum(child_lines.with_context(for_parent=True)._get_cost_price())
        # ~ elif self._context.get('for_parent', False):
            # ~ if self.purchase_price and self.product_uom_qty:
                # ~ cost_price = self.purchase_price * self.product_uom_qty
            # ~ elif self.product_id.standard_price:
                # ~ cost_price = self.product_id.standard_price * self.product_uom_qty
        # ~ elif not self.pack_parent_line_id:
            # ~ if self.purchase_price and self.product_uom_qty:
                # ~ cost_price = self.purchase_price
            # ~ elif self.product_id.standard_price:
                # ~ cost_price = self.product_id.standard_price
        return cost_price

    @api.one
    @api.depends('product_id', 'price_unit', 'product_uom_qty', 'purchase_price', 'discount')
                 #TODO: Migrar'pack_child_line_ids', 'pack_parent_line_id')
    def _product_margin(self):
        margin = 0.0
        if self.product_id:
            cost_price = self._get_cost_price()[0]
        else:
            cost_price = self.purchase_price
        if cost_price:
            margin = round((self.price_unit * self.product_uom_qty *
                           (100.0 - self.discount) / 100.0) -
                           (cost_price * self.product_uom_qty), 2)
            self.margin_perc = round((margin * 100) /
                                                (cost_price * self.product_uom_qty), 2)
        self.margin = margin

    margin = fields.Float('Margin', compute='_product_margin', store=True)
    margin_perc = fields.Float('Margin', compute='_product_margin', store=True)
