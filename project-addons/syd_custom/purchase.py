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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    shipment_count_ = fields.Integer('Incoming Shipments',
                                     compute='_count_ship', store=True)
    #carrier = fields.Char('Carrier')
    carrier = fields.Many2one('delivery.carrier','Carrier')

    @api.depends('picking_ids')
    def _count_ship(self):
        for po in self:
            po.shipment_count_ = len([x.id for x in po.picking_ids
                                      if x.state not in ['cancel']])
