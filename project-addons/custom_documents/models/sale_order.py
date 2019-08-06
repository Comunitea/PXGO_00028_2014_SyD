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
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    title = fields.Char('name')
    baseline_data = fields.Text('starting data indicated by the client')
    have_discounts = fields.Boolean('Have discounts', compute='_have_discounts')

    @api.one
    def _have_discounts(self):
        discounts = False
        for line in self.order_line:
            if line.discount > 0:
                discounts = True
        self.have_discounts = discounts


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    price_unit_net = fields.Float('Unit Price',
                                  digits= dp.get_precision('Product Price'),
                                  compute='_get_price_unit_net')

    @api.one
    @api.depends('price_unit', 'discount')
    def _get_price_unit_net(self):
        self.price_unit_net = self.price_unit * (1 - (self.discount / 100))


