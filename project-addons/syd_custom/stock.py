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

    supplier_ref = fields.Char('Supplier reference', copy=False)

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

        for invoice in invoice_ids:
            write_vals = {}
            invoice_obj = self.env['account.invoice'].browse(invoice)
            has_supp_ref = invoice_obj.picking_ids.filtered(
                lambda record: record.supplier_ref and True or False)
            supplier_ref_list = has_supp_ref.mapped('supplier_ref')
            if supplier_ref_list:
                write_vals['supplier_picking_ref'] = ', '.join(
                    list(set(supplier_ref_list)))

            has_order_ref = invoice_obj.picking_ids.filtered(
                lambda record: record.sale_id.client_order_ref and True or
                False)
            name_list = has_order_ref.mapped('sale_id.client_order_ref')
            if name_list:
                write_vals['name'] = ', '.join(list(set(name_list)))
            if write_vals:
                invoice_obj.write(write_vals)

        return invoice_ids
