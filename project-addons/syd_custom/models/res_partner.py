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
from odoo import models, api


class res_partner(models.Model):

    _inherit = 'res.partner'

    def _compute_sale_order_count(self):
        for partner in self:
            sales_no = self.env['sale.order'].search_count(
                domain=[('partner_id', 'child_of', [partner.id])])
            partner.sale_order_count = sales_no

    def _get_meeting_len(self):
        self.ensure_one()
        total = 0
        if self.child_ids:
            for child in self.child_ids:
                total += child._get_meeting_len()
        return total + len(self.meeting_ids)

    @api.multi
    def _compute_meeting_count(self):
        for partner in self:
            partner.meeting_count = partner._get_meeting_len()

    @api.multi
    def _compute_phonecall_count(self):
        for partner in self:
            partner.phonecall_count = self.env[
                'crm.phonecall'].search_count(
                [('partner_id', 'child_of', [partner.id])])

    @api.model
    def create(self, vals):
        if not vals.get('ref', False):
            vals['ref'] = self.env['ir.sequence'].next_by_code('res.partner')
        return super().create(vals)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        if not default.get('ref'):
            default['ref'] = self.env['ir.sequence'].\
                next_by_code('res.partner')
        return super().copy(default)
