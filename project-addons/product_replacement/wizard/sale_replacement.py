# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Pexego All Rights Reserved
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
from openerp import models, fields, api


class SaleAddReplacementLine(models.TransientModel):

    _name = 'sale.add.replacement.line'

    wizard_id = fields.Many2one('sale.replacement', 'wizard')
    product_id = fields.Many2one('product.product', 'Product')
    disassembly_ref = fields.Char('Disassembly reference')
    qty = fields.Float('Quantity')
    qty_in = fields.Float('Quantity')


class SaleAddReplacement(models.TransientModel):

    _name = 'sale.add.replacement'
    product_id = fields.Many2one('product.product', 'Product')
    line_ids = fields.One2many('sale.add.replacement.line', 'wizard_id',
                               'Lines')

    @api.multi
    def add_replacement(self):
        for line in self.line_ids:
            if line.qty_in > 0:
                self.env['sale.order.line'].create({
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.qty_in,
                    'order_id': self.env.context.get('active_id')
                })
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('product_id')
    def onchange_product_id(self):
        lines = []
        for replacement in self.product_id.replacement_ids:
            lines.append(
                (0, 0, {'product_id': replacement.product_id.id,
                        'disassembly_ref': replacement.disassembly_ref,
                        'qty': replacement.qty}))
        self.line_ids = lines
