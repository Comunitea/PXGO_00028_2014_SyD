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
from odoo import models, fields, api, exceptions, _


class SaleOrderUpdatePurchasePriceLine(models.TransientModel):

    _name = 'sale.order.update.purchase.price.line'

    order_line_id = fields.Many2one('sale.order.line', 'Order line')
    product_id = fields.Many2one('product.product', 'Product')
    purchase_price = fields.Float('Purchase price')
    wizard_id = fields.Many2one('sale.order.update.purchase.price', 'wzd')


class SaleOrderUpdatePurchasePrice(models.TransientModel):

    _name = 'sale.order.update.purchase.price'

    wizard_lines = fields.One2many('sale.order.update.purchase.price.line',
                                   'wizard_id', 'Lines')

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderUpdatePurchasePrice, self).default_get(fields)
        sale_id = self._context.get('active_id')
        if sale_id and not self.env.context.get('nocreate', False):
            sale = self.env['sale.order'].browse(sale_id)
            lines = []
            for line in sale.order_line:
                if line.product_id:
                    lines.append((0, 0, {'order_line_id': line.id,
                                         'purchase_price': line.purchase_price,
                                         'product_id': line.product_id.id,
                                         }))
            if lines:
                res.update(wizard_lines=lines)
        return res

    @api.multi
    def set_purchase_price_by_order(self):
        self.ensure_one()
        for line in self.wizard_lines:
            procurement_group = line.order_line_id.order_id.procurement_group_id
            procurements = self.env['procurement.order'].search(
                [('group_id', '=', procurement_group.id),
                 ('purchase_line_id', '!=', False),
                 ('product_id', '=', line.order_line_id.product_id.id)])
            procurement = procurements and procurements[0] or False
            if procurement:
                line.purchase_price = procurement.purchase_line_id.price_unit
        context = dict(self.env.context)
        context.update(nocreate=True)
        return {
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.update.purchase.price',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def update(self):
        self.ensure_one()
        for line in self.wizard_lines:
            line.order_line_id.purchase_price = line.purchase_price
        return {'type': 'ir.actions.act_window_close'}
