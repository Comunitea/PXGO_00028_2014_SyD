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
from openerp import models, api, _, fields


class sale_order(models.Model):

    _inherit = 'sale.order'

    def print_quotation(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        return self.pool['report'].get_action(cr, uid, ids, 'sale.report_saleorder', context=context)

    def quotation_sended(self, cr, uid, ids, context=None):
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        return True


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change_with_wh(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False, warehouse_id=False):
        warning = {}
        if not product:
            return {'value': {'th_weight' : 0, 'product_packaging': False,
                'product_uom_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        product_obj = self.env['product.product']
        product_info = product_obj.browse(product)
        title = False
        message = False

        if product_info.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product_info.name
            message = product_info.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            if product_info.sale_line_warn == 'block':
                return {'value': {'product_id': False}, 'warning': warning}

        result =  super(SaleOrderLine, self).product_id_change_with_wh(pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag, warehouse_id=warehouse_id)
        result.pop('warning', None)
        if result.get('warning',False):
            warning['title'] = title and title +' & '+result['warning']['title'] or result['warning']['title']
            warning['message'] = message and message +'\n\n'+result['warning']['message'] or result['warning']['message']

        if warning:
            result['warning'] = warning
        return result


class sale_report(models.Model):
    _inherit = "sale.report"

    margin = fields.Float()

    def _select(self):
        select_str = super(sale_report,self)._select()
        this_str = """, l.margin as margin"""
        return select_str + this_str

    def _group_by(self):
        group_by_str = super(sale_report,self)._group_by()
        this_str = """, l.margin"""
        return group_by_str + this_str
