# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Pexego All Rights Reserved
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
import openerp.addons.decimal_precision as dp


class StockMoveService(models.Model):

    _name = 'stock.move.service'

    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity = fields.Float('Quantity', digits= dp.get_precision('Product Unit of Measure'))
    product_uom = fields.Many2one('product.uom', 'UoM')
    picking_id = fields.Many2one('stock.picking', 'Picking')
    sale_line_id = fields.Many2one('sale.order.line', 'Order line')


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    service_ids = fields.One2many('stock.move.service', 'picking_id',
                                  'Services')

    @api.one
    def get_services(self):
        services = self.env['stock.move.service']
        self.service_ids.unlink()
        for line in self.sale_id.order_line:
            if line.product_id.type == 'service':
                services += services.create({'product_id': line.product_id.id,
                                             'product_uom':
                                            line.product_uom.id,
                                             'quantity': line.product_uom_qty,
                                             'sale_line_id': line.id})
        self.service_ids = services
