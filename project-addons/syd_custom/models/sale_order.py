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
from odoo import models, fields, api, exceptions, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def print_quotation(self):
        return self.env.ref('sale.action_report_saleorder').report_action(self)

    @api.multi
    def quotation_sended(self):
        return self.filtered(lambda s: s.state == 'draft').\
            write({'state': 'sent'})

    @api.multi
    def action_confirm(self):
        if self.order_line.filtered(lambda s: s.product_id ==
                                    self.env.
                                    ref('syd_custom.product_wildcard')):
            raise exceptions.UserError(_("Cannot confirm an order with "
                                         "wildcard products"))
        return super().action_confirm()

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if invoice_vals.get('comment'):
            del invoice_vals['comment']
        return invoice_vals

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        invoices = super().action_invoice_create(grouped=grouped,
                                                 final=final)
        for invoice in self.env['account.invoice'].browse(invoices).\
                filtered(lambda x: x.type == 'out_refund'):
            sales = invoice.mapped('invoice_line_ids.sale_line_ids.order_id')
            for sale in sales:
                order_invoices = sale.invoice_ids.\
                    filtered(lambda x: x.type == 'out_invoice' and
                             not x.refund_invoice_ids)
                if order_invoices:
                    invoice.refund_invoice_id = order_invoices[0].id

        return invoices


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    product_id = fields.\
        Many2one(default=lambda self:
                 self.env.ref('syd_custom.product_wildcard'))


class SaleAdvancePaymentInv(models.TransientModel):

    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super()._create_invoice(order, so_line, amount)
        if invoice.comment:
            invoice.comment = False
        return invoice
