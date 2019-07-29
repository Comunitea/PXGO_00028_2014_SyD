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
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_ship_create(self, cr, uid, ids, context=None):
        procurement_obj = self.pool.get('procurement.order')
        sale_line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids, context=context):

            for line in order.order_line:
                #Try to fix exception procurement (possible when after a shipping exception the user choose to recreate)
                if line.procurement_ids:
                    for proc in line.procurement_ids:
                    #first check them to see if they are in exception or not (one of the related moves is cancelled)
                        if proc.state == 'cancel':
                            procurement_obj.write(cr, uid, proc.id,
                                              {'product_id':
                                                   line.product_id.id,
                                               'product_qty':
                                                   line.product_uom_qty,
                                               'product_uom_qty':
                                                   line.product_uom_qty
                                               })
                else:
                    if line.state == 'draft':
                        sale_line_obj.write(cr, uid, line.id,
                            {'state': 'confirmed'})

        super(SaleOrder, self).action_ship_create(cr, uid, ids,
                                                   context=context)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def unlink(self, cr, uid, ids, context=None):
        self.button_cancel(cr, uid, ids, context)
        return super(SaleOrderLine, self).unlink(cr, uid, ids, context=context)
