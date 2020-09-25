##############################################################################
#
#    Copyright (C) 2014 Comunitea Servicios Tecnológicos All Rights Reserved
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

from odoo import models, fields, api


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.depends('margin')
    @api.multi
    def _product_margin_perc(self):
        for sale in self:
            if sale.amount_untaxed:
                sale.margin_perc = round((sale.margin * 100) /
                                         sale.amount_untaxed, 2)

    @api.depends('order_line')
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


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.depends('margin', 'purchase_price', 'product_id')
    def _product_margin_perc(self):
        for line in self:
            if line.purchase_price:
                cost_price = line.purchase_price
            else:
                cost_price = line.product_id.standard_price
            if cost_price and line.product_uom_qty:
                line.margin_perc = round((line.margin * 100) /
                                         (cost_price * line.product_uom_qty),
                                         2)

    margin_perc = fields.Float('Margin', compute='_product_margin_perc',
                               store=True)
