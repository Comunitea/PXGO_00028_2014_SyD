##############################################################################
#
#    Copyright (C) 2019 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
#    $Omar Castiñeira Saavedra <omar@comunitea.com>$
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
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    replacement_for_id = fields.Many2one('stock.production.lot',
                                         'Replacement for')


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    replacement_sent_ids = fields.One2many('stock.move.line',
                                           'replacement_for_id',
                                           'Replacements sent')


class StockMove(models.Model):

    _inherit = "stock.move"

    def _compute_show_details_visible(self):
        super()._compute_show_details_visible()
        for move in self:
            if move.product_id and move.product_id.replacement_for_ids:
                move.show_details_visible = True
