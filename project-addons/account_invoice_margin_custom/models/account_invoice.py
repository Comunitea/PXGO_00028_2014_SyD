
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    margin_company_currency = fields.Float(
        string='Margin in Company Currency',
        readonly=True, compute='_compute_margin', store=True,
        digits=dp.get_precision('Account'))
    margin_percent = fields.Float("% Margin", readonly=True,
                                  compute='_compute_margin', store=True,
                                  digits=dp.get_precision('Account'))

    @api.one
    @api.depends('type', 'invoice_line_ids.margin')
    def _compute_margin(self):
        margin_comp_cur = 0.0
        subtotal = 0.0
        if self.type in ('out_invoice', 'out_refund'):
            for il in self.invoice_line_ids:
                margin_comp_cur += il.margin
                subtotal += il.price_subtotal
        self.margin_company_currency = margin_comp_cur
        self.margin_percent = (margin_comp_cur / subtotal * 100.0 if subtotal
                               else 0.0)
