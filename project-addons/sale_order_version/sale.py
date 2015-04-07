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


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    version = fields.Integer('Version')
    new_version_id = fields.Many2one('sale.order', 'New version')
    orig_version_id = fields.Many2one('sale.order', 'Original version')



    name = fields.Char(states={'draft': [('readonly', False)]})
    date_order = fields.Datetime(states={'draft': [('readonly', False)]})
    user_id = fields.Many2one(states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one(states={'draft': [('readonly', False)]})
    partner_invoice_id = fields.Many2one(states={'draft': [('readonly', False)]})
    partner_shipping_id = fields.Many2one(states={'draft': [('readonly', False)]})
    order_policy = fields.Selection(states={'draft': [('readonly', False)]})
    pricelist_id = fields.Many2one(states={'draft': [('readonly', False)]})
    project_id = fields.Many2one(states={'draft': [('readonly', False)]})
    order_line = fields.One2many(states={'draft': [('readonly', False)]})
    ship_id = fields.Many2one(states={'draft': [('readonly', False)]})


    @api.one
    def create_new_version(self):
        new_version = self.copy({'version': self.version + 1, 'orig_version_id': self.id})
        new_version.write({'name': new_version.name + ' V' + str(new_version.version)})
        self.new_version_id = new_version.id
        self.signal_workflow('cancel')
