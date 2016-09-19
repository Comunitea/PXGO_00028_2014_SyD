# -*- coding: utf-8 -*-
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
from openerp.osv import fields, osv
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class sale_order(osv.osv):

    _inherit = 'sale.order'

    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        order_confirm_datetime = datetime.strptime(order.date_confirm + " 06:00:00", DEFAULT_SERVER_DATETIME_FORMAT)
        dc_s = order_confirm_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        date_planned = super(sale_order, self)._get_date_planned(cr, uid, order, line, dc_s, context=context)
        print date_planned
        return date_planned
        
    # Calcula fecha de compromiso desde la fecha de confirmación si ya  existe   
    def _get_commitment_date(self, cr, uid, ids, name, arg, context=None):
        """Compute the commitment date"""
        res = {}
        dates_list = []
        for order in self.browse(cr, uid, ids, context=context):
            dates_list = []
            if order.date_confirm:
                print "Compromiso sobre confirmación"
                order_datetime = datetime.strptime(order.date_confirm + " 06:00:00", DEFAULT_SERVER_DATETIME_FORMAT)
            else:
                order_datetime = datetime.strptime(order.date_order, DEFAULT_SERVER_DATETIME_FORMAT)
            for line in order.order_line:
                if line.state == 'cancel':
                    continue
                dt = order_datetime + timedelta(days=line.delay or 0.0)
                dt_s = dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                dates_list.append(dt_s)
            if dates_list:
                res[order.id] = min(dates_list)
        return res
        
    _columns = {
        'commitment_date': fields.function(_get_commitment_date, store=True,
            type='datetime', string='Commitment Date',
            help="Date by which the products are sure to be delivered. This is "
                 "a date that you can promise to the customer, based on the "
                 "Product Lead Times."),
    }
