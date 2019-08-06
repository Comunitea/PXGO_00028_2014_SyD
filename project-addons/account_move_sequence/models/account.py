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


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        res = super().action_move_create()
        for invoice in self:
            move_lines = self.env['account.move.line'].search(
                [('move_id', '=', invoice.move_id.id)])
            sequence = 1
            for line in move_lines:
                line.sequence = sequence
                sequence += 1
        return res


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    sequence = fields.Integer('Sequence')
