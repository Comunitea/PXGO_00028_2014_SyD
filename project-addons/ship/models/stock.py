##############################################################################
#
#    Copyright (C) 2014 Comunitea All Rights Reserved
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
from odoo import models, fields


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    ship_id = fields.Many2one('ship', 'Ship')


class StockMove(models.Model):

    _inherit = "stock.move"

    def _assign_picking_post_process(self, new=False):
        super()._assign_picking_post_process(new=new)
        if new and self.sale_line_id and self.sale_line_id.order_id.ship_id:
            self.picking_id.ship_id = self.sale_line_id.order_id.ship_id
