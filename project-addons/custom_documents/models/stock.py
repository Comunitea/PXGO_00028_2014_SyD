##############################################################################
#
#    Copyright (C) 2019 Comunitea Servicios Tecnológicos. All Rights Reserved
#    $Omar Castiñeira Saavedra$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):

    _inherit = "stock.picking"

    amount_gross = fields.Monetary('Amount gross', compute='_amount_all',
                                   compute_sudo=True)
    amount_discounted = fields.Monetary('Sale price', compute='_amount_all',
                                        compute_sudo=True)
    external_note = fields.Text('External Notes')

    @api.multi
    def get_taxes_values(self):
        tax_grouped = super().get_taxes_values()
        for line in self.service_ids:
            for tax in line.sale_line_id.tax_id:
                tax_id = tax.id
                price_unit = line.sale_line_id.price_unit * \
                    (1 - (line.sale_line_id.discount or 0.0) / 100.0)
                if tax_id not in tax_grouped:
                    tax_grouped[tax_id] = {
                        'base': price_unit * line.quantity,
                        'tax': tax,
                    }
                else:
                    tax_grouped[tax_id]['base'] += price_unit * line.quantity
        for tax_id, tax_group in tax_grouped.items():
            tax_grouped[tax_id]['amount'] = tax_group['tax'].compute_all(
                tax_group['base'], self.sale_id.currency_id
            )['taxes'][0]['amount']
        return tax_grouped

    @api.multi
    def _amount_all(self):
        for picking in self:
            if not picking.sale_id:
                picking.amount_discounted = picking.amount_gross = 0.0
                continue
            amount_gross = 0.0
            for line in picking.move_lines:
                sale_line = line.sale_line_id
                if sale_line and line.state != 'cancel':
                    amount_gross += (line.sale_line_id.price_unit *
                                     line.product_qty)
                else:
                    continue
            for line in picking.service_ids:
                sale_line = line.sale_line_id
                if sale_line:
                    amount_gross += (sale_line.price_unit *
                                     line.quantity)
                else:
                    continue
            round_curr = picking.sale_id.currency_id.round
            picking.amount_gross = round_curr(amount_gross)
            picking.amount_discounted = round_curr(amount_gross) - \
                picking.amount_untaxed


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    sale_price_unit_net = fields.Float(
        related='sale_line.price_unit_net', readonly=True,
        string='Sale price unit',
        related_sudo=True,
    )


class StockMoveService(models.Model):

    _inherit = 'stock.move.service'

    price_subtotal = fields.Float(
        compute='_get_subtotal', string="Subtotal",
        digits=dp.get_precision('Sale Price'), readonly=True,
        store=False)
    order_price_unit = fields.Float(
        compute='_get_subtotal', string="Price unit",
        digits=dp.get_precision('Sale Price'), readonly=True,
        store=False)
    order_price_unit_net = fields.Float(
        compute='_get_subtotal', string="Price unit",
        digits=dp.get_precision('Sale Price'), readonly=True,
        store=False)
    discount = fields.Float(
        compute='_get_subtotal', string="Discount",
        digits=dp.get_precision('Discount'), readonly=True,
        store=False)
    cost_subtotal = fields.Float(
        compute='_get_subtotal', string="Cost subtotal",
        digits=dp.get_precision('Sale Price'), readonly=True,
        store=False)
    margin = fields.Float(
        compute='_get_subtotal', string="Margin",
        digits=dp.get_precision('Sale Price'), readonly=True,
        store=False)
    percent_margin = fields.Float(
        compute='_get_subtotal', string="% margin",
        digits=dp.get_precision('Sale Price'), readonly=True,
        store=False)

    @api.multi
    def _get_subtotal(self):
        for service in self:
            if service.sale_line_id:
                cost_price = service.sale_line_id.purchase_price or \
                    service.product_id.standard_price or 0.0
                price_unit = (service.sale_line_id.price_unit *
                              (1-(service.sale_line_id.discount or
                                  0.0)/100.0))
                service.price_subtotal = price_unit * service.quantity
                service.order_price_unit = service.sale_line_id.price_unit
                service.discount = service.sale_line_id.discount
                service.order_price_unit_net = price_unit
                service.cost_subtotal = cost_price * service.quantity
                service.margin = service.price_subtotal - service.cost_subtotal
                if service.price_subtotal > 0:
                    service.percent_margin = (service.margin /
                                              service.price_subtotal) * 100
                else:
                    service.percent_margin = 0
            else:
                service.price_subtotal = 0.0
                service.discount = 0.0
                service.order_price_unit = 0.0
                service.order_price_unit_net = 0.0
                service.cost_subtotal = 0.0
                service.margin = 0.0
                service.percent_margin = 0.0
