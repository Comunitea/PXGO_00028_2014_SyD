# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Pexego All Rights Reserved
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


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    ship_id = fields.Many2one('ship', 'Ship', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    partner_parent_id = fields.Many2one('res.partner', 'partner parent', compute='_get_partner_parent')

    @api.depends('partner_id')
    def _get_partner_parent(self):
        for sale in self:
            if not sale.partner_id.parent_id:
                sale.partner_parent_id = sale.partner_id
            else:
                sale.partner_parent_id = sale.partner_id.parent_id

    @api.multi
    def action_ship_create(self):
        res = super(SaleOrder, self).action_ship_create()
        for order in self:
            if not order.ship_id:
                continue
            pickings = self.env['stock.picking']
            for line in order.order_line:
                for procurement in line.procurement_ids:
                    for move in procurement.move_ids:
                        if move.picking_id not in pickings:
                            pickings += move.picking_id
            pickings.write({'ship_id': order.ship_id.id})
        return res

    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(SaleOrder, self)._prepare_invoice(order, lines)
        res['ship_id'] = order.ship_id.id
        return res
