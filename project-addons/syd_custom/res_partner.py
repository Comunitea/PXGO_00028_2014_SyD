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
from openerp import models
from openerp.osv import fields,osv


class res_partner(osv.osv):

    _inherit = 'res.partner'

    def _sale_order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        # The current user may not have access rights for sale orders
        try:
            for partner in self.browse(cr, uid, ids, context):
                res[partner.id] = len(self.pool.get('sale.order').search(cr, uid, [('partner_id', 'child_of', partner.id)], context=context))
        except:
            pass
        return res

    def _get_meeting_len(self, cr, uid, partner, context={}):
        total = 0
        if partner.child_ids:
            for child in partner.child_ids:
                total += self._get_meeting_len(cr, uid, child, context)
        return total + len(partner.meeting_ids)


    def _opportunity_meeting_phonecall_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,{'opportunity_count': 0, 'meeting_count': 0}), ids))
        # the user may not have access rights for opportunities or meetings
        try:
            for partner in self.browse(cr, uid, ids, context):
                if partner.is_company:
                    operator = 'child_of'
                else:
                    operator = '='
                opp_ids = self.pool['crm.lead'].search(cr, uid, [('partner_id', operator, partner.id), ('type', '=', 'opportunity'), ('probability', '<', '100')], context=context)
                phonnecall_ids = self.pool['crm.phonecall'].search(cr, uid, [('partner_id', operator, partner.id)], context=context)
                res[partner.id] = {
                    'opportunity_count': len(opp_ids),
                    'meeting_count': self._get_meeting_len(cr, uid, partner, context),
                    'phonecall_count': len(phonnecall_ids),
                }
        except:
            pass
        return res

    _columns = {
        'sale_order_count': fields.function(_sale_order_count, string='# of Sales Order', type='integer'),
        'opportunity_count': fields.function(_opportunity_meeting_phonecall_count, string="Opportunity", type='integer', multi='opp_meet'),
        'meeting_count': fields.function(_opportunity_meeting_phonecall_count, string="# Meetings", type='integer', multi='opp_meet'),
        'phonecall_count': fields.function(_opportunity_meeting_phonecall_count, string="Phonecalls", type="integer", multi='opp_meet'),
        'title': fields.many2one('res.partner.title', 'Calification'),
    }

    def create(self, cr, uid, vals, context=None):
        if not vals.get('ref', False):
            vals['ref'] = self.pool.get('ir.sequence').get(cr, uid,
                                                           'res.partner')
        return super(res_partner, self).create(cr, uid, vals, context)

    def copy(self, cr, uid, id, default=None, context=None):
        if not default.get('ref', False):
            default['ref'] = self.pool.get('ir.sequence').get(cr, uid,
                                                              'res.partner')
        return super(res_partner, self).copy(cr, uid, id, default, context)
