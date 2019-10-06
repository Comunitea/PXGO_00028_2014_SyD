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
from odoo import models, api, fields, exceptions, _
import time


class res_partner(models.Model):

    _inherit = 'res.partner'

    total_invoiced_current_year = fields.\
        Monetary(compute='_invoice_total_curr_year', string="Total Invoiced",
                 groups='account.group_account_invoice')

    @api.multi
    @api.constrains('phone', 'name', 'parent_id')
    def _check_phone_set(self):
        for partner in self:
            if not partner.parent_id and not partner.phone:
                raise exceptions.\
                    ValidationError(_("Please set the phone field"))

    @api.multi
    def _invoice_total_curr_year(self):
        account_invoice_report = self.env['account.invoice.report']
        if not self.ids:
            self.total_invoiced_current_year = 0.0
            return True

        all_partners_and_children = {}
        all_partner_ids = []
        for partner in self:
            all_partners_and_children[partner] = self.\
                with_context(active_test=False).\
                search([('id', 'child_of', partner.id)]).ids
            all_partner_ids += all_partners_and_children[partner]

        where_query = account_invoice_report._where_calc([
            ('partner_id', 'in', all_partner_ids),
            ('state', 'not in', ['draft', 'cancel']),
            ('type', 'in', ('out_invoice', 'out_refund')),
            ('date', '>=', time.strftime("%Y-01-01"))
        ])
        account_invoice_report._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        # price_total is in the company currency
        query = """
                  SELECT SUM(price_total) as total, partner_id
                    FROM account_invoice_report account_invoice_report
                   WHERE %s
                   GROUP BY partner_id
                """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            partner.total_invoiced_current_year = \
                sum(price['total'] for price in
                    price_totals if price['partner_id'] in child_ids)

    def _compute_sale_order_count(self):
        for partner in self:
            sales_no = self.env['sale.order'].search_count(
                [('partner_id', 'child_of', [partner.id])])
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
