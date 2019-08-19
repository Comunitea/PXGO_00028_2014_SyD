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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('picking_ids.state', 'picking_ids.supplier_ref')
    def _get_supplier_pick_refs(self):
        for purchase in self:
            refs = []
            for pick in purchase.picking_ids:
                if pick.supplier_ref and pick.state == 'done' \
                        and pick.supplier_ref not in refs:
                    refs.append(pick.supplier_ref)
            if refs:
                purchase.supplier_picking_ref = " // ".join(refs)

    shipment_count_ = fields.Integer('Incoming Shipments',
                                     compute='_count_ship', store=True)
    carrier = fields.Many2one('delivery.carrier', 'Carrier')
    supplier_picking_ref = fields.Text("Supplier picking refs.", store=True,
                                       compute="_get_supplier_pick_refs")

    @api.depends('picking_ids.state')
    def _count_ship(self):
        for po in self:
            po.shipment_count_ = len([x.id for x in po.picking_ids
                                      if x.state not in ['cancel']])

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('name', operator, name),
                      ('partner_ref', operator, name),
                      ('supplier_picking_ref', operator, name)]
        pos = self.search(domain + args, limit=limit)
        return pos.name_get()
