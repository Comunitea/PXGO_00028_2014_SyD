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
from openerp import models, fields, api


class crm_lead(models.Model):

    _inherit = 'crm.lead'

    purchase_ids = fields.Many2many('purchase.order',
                                    'lead_purchase_order_rel', 'lead_id',
                                    'purchase_id', 'Related purchases')


class crm_make_sale(models.TransientModel):

    _inherit = "crm.make.sale"

    @api.multi
    def makeOrder(self):
        lead = self.env['crm.lead'].browse(self.env.context.get('active_id', False))
        res = super(crm_make_sale, self).makeOrder()
        sale_ids = res['res_id']
        if not isinstance(sale_ids, (int, long, type([]))):
            return res
        for sale in self.env['sale.order'].browse(sale_ids):
            sale.purchase_ids = lead.purchase_ids
        return res
