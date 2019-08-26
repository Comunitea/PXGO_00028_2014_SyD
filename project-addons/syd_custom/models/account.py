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

    supplier_picking_ref = fields.Char('Supplier picking reference')
    payment_order_count = fields.Integer("# Payment Order", store=True,
                                         compute="_get_payment_order_count")

    @api.multi
    @api.depends('move_id.line_ids.payment_line_ids')
    def _get_payment_order_count(self):
        for invoice in self:
            if invoice.move_id:
                invoice.payment_order_count = \
                    len(invoice.move_id.mapped('line_ids.payment_line_ids'))

    @api.onchange('invoice_line_ids')
    def _onchange_origin(self):
        super()._onchange_origin()
        purchase_ids = self.invoice_line_ids.mapped('purchase_id')
        if purchase_ids:
            self.supplier_picking_ref = ', '.\
                join(purchase_ids.mapped('supplier_picking_ref'))

    @api.multi
    def action_view_payment_orders(self):
        self.ensure_one()
        payment_orders = []
        if self.move_id:
            payment_orders = self.move_id.\
                mapped('line_ids.payment_line_ids.order_id')
        action = (
            self.env.
            ref('account_payment_order.account_payment_order_inbound_action').
            read()[0])
        action['domain'] = []
        if payment_orders:
            action['domain'] = [('id', 'in', payment_orders.ids)]
        return action


class AccountInvoiceReport(models.Model):

    _inherit = 'account.invoice.report'

    payment_mode_id = fields.Many2one('account.payment.mode', 'Payment mode')
    number = fields.Char('Number')

    def _select(self):
        select_str = super()._select()
        select_str += ', sub.payment_mode_id as payment_mode_id,' \
                      ' sub.number as number'
        return select_str

    def _sub_select(self):
        select_str = super()._sub_select()
        select_str += ', ai.payment_mode_id,' \
                      ' ai.number'
        return select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ', ai.payment_mode_id, ai.number'

        return group_by_str
