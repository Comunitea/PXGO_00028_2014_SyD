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
from openerp import models, fields, api, exceptions, _


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    supplier_ref = fields.Char('Supplier reference')

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        res = super(StockPicking, self)._get_invoice_vals(key, inv_type,
                                                        journal_id, move)
        res['supplier_picking_ref'] = move.picking_id.supplier_ref
        return res

    @api.multi
    def action_invoice_create(self, journal_id, group=False,
                              type='out_invoice'):
        invoice_ids = super(StockPicking, self).action_invoice_create(
                                    journal_id, group=group, type=type)

        # import ipdb; ipdb.set_trace()

        for invoice in invoice_ids:
            invoice_obj = self.env['account.invoice'].browse(invoice)
            supp_pick_ref = ''
            if(invoice_obj):
                for pick in invoice_obj.picking_ids:
                    if(pick.supplier_ref):
                        if(supp_pick_ref):
                            supp_pick_ref += ', '
                        supp_pick_ref += pick.supplier_ref
            invoice_obj.supplier_picking_ref = supp_pick_ref

        return invoice_ids
