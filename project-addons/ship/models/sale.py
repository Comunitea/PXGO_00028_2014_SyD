##############################################################################
#
#    Copyright (C) 2014 Comunitea All Rights Reserved
#    $Jesús Ventosinos Mayor <jesus@comunitea.com>$
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
from odoo import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    ship_id = fields.Many2one('ship', 'Ship', readonly=True,
                              states={'draft': [('readonly', False)],
                                      'sent': [('readonly', False)]})
    partner_parent_id = fields.\
        Many2one('res.partner', 'partner parent', readonly=True,
                 related='partner_id.commercial_partner_id')

    @api.multi
    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['ship_id'] = self.ship_id.id
        return res
