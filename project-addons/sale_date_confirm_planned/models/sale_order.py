##############################################################################
#
#    Copyright (C) 2016 Comunitea All Rights Reserved
#    $Santi Argüeso <santi@comunitea.com>$
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
from odoo import fields, models, api
from datetime import timedelta


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.depends('date_order', 'order_line.customer_lead', 'confirmation_date')
    def _compute_commitment_date(self):
        """Compute the commitment date"""
        for order in self:
            dates_list = []
            if order.confirmation_date:
                order_datetime = fields.Datetime.\
                    from_string(order.confirmation_date)
            else:
                order_datetime = fields.Datetime.from_string(order.date_order)
            for line in order.order_line.\
                filtered(lambda x: x.state != 'cancel' and
                         not x._is_delivery()):
                dt = order_datetime + timedelta(days=line.customer_lead or 0.0)
                dates_list.append(dt)
            if dates_list:
                commit_date = min(dates_list) \
                    if order.picking_policy == 'direct' else max(dates_list)
                order.commitment_date = fields.Datetime.to_string(commit_date)
