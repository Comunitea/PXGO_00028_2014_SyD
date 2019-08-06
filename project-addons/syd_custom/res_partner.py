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
from odoo import models, fields, api


class res_partner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    def _sale_order_count(self):
        for partner in self:
            partner.sale_order_count = self.env['sale.order'].\
                search_count([('partner_id', 'child_of', [partner.id])])

    def _get_meeting_len(self):
        self.ensure_one()
        total = 0
        if self.child_ids:
            for child in self.child_ids:
                total += child._get_meeting_len()
        return total + len(self.meeting_ids)

    @api.multi
    def _opportunity_meeting_phonecall_count(self):
        for partner in self:
            if partner.is_company:
                operator = 'child_of'
            else:
                operator = '='
            opps = self.env['crm.lead'].\
                search_count([('partner_id', operator, partner.id),
                              ('type', '=', 'opportunity'),
                              ('probability', '<', '100')])
            phonnecalls = self.env['crm.phonecall'].\
                search_count([('partner_id', operator, partner.id)])
            partner.opportunity_count = opps
            partner.meeting_count = partner._get_meeting_len()
            partner.phonecall_count = phonnecalls

    sale_order_count = fields.Integer(compute="_sale_order_count",
                                      string='# of Sales Order')
    opportunity_count = fields.\
        Integer(compute="_opportunity_meeting_phonecall_count",
                string="Opportunity", multi=True)
    meeting_count = fields.\
        Integer(compute="_opportunity_meeting_phonecall_count",
                string="# Meetings", multi=True)
    phonecall_count = fields.\
        Integer(compute="_opportunity_meeting_phonecall_count",
                string="Phonecalls", multi=True)

    @api.model
    def create(self, vals):
        if not vals.get('ref', False):
            vals['ref'] = self.env['ir.sequence'].next_by_code('res.partner')
        return super(res_partner, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if not default.get('ref', False):
            default['ref'] = self.env['ir.sequence'].\
                next_by_code('res.partner')
        return super(res_partner, self).copy(default)
