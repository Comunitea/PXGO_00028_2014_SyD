##############################################################################
#
#    Copyright (C) 2020 Comunitea All Rights Reserved
#    Vicente Ángle Gutiérrez Fernández <vicente@comunitea.com>
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

from odoo import api, models

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    def get_new_formated_lot(self, picking=None):
        if not picking or not self.product_id.tracking == 'serial':
            return self.lot_formatted_note
        else:
            lot_formatted_note = "S/N: {}".format(picking.move_line_ids.filtered(lambda x: x.product_id.id == x.product_id.id).mapped('lot_id').name)
            return lot_formatted_note
        