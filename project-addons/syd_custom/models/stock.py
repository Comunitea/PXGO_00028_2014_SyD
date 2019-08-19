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
from odoo import models, fields, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    supplier_ref = fields.Char('Supplier reference', copy=False)


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    product_available = fields.\
        Float('Quantity available',
              compute='_compute_product_available', search='_search_total')

    @api.multi
    def _compute_product_available(self):
        for lot in self:
            lot.product_available = lot.product_id.qty_available

    @api.model
    def _search_total(self, operator, operand):
        return [
            ('id',
             'in',
             self.search(
                [('product_id.qty_available', operator, operand)]).ids)]
