##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comuniutea.com>$
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
from odoo import models


class ProcurementRule(models.Model):

    _inherit = "procurement.rule"

    def _prepare_purchase_order(self, product_id, product_qty, product_uom,
                                origin, values, partner):
        vals = super().\
            _prepare_purchase_order(product_id, product_qty, product_uom,
                                    origin, values, partner)
        if values.get('move_dest_ids') and \
                values['move_dest_ids'][0].sale_line_id:
            line = values['move_dest_ids'][0].sale_line_id
            vals.update({'customer_id': line.order_id.partner_id.id,
                         'sale_ids': [(6, 0, [line.order_id.id])],
                         'lead_ids': line.order_id.opportunity_id and
                         [(6, 0, [line.order_id.opportunity_id.id])]
                         or False})
        return vals
