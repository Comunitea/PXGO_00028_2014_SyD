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
from openerp import models, fields


class purchase_order(models.Model):

    _inherit = 'purchase.order'

    customer_id = fields.Many2one('res.partner', 'Customer')
    sale_ids = fields.Many2many('sale.order', 'sale_purchase_order_rel',
                                'purchase_id', 'sale_id', 'related Sales')
    lead_ids = fields.Many2many('crm.lead', 'lead_purchase_order_rel',
                                'purchase_id', 'lead_id', 'Related leads')
