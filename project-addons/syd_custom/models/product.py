##############################################################################
#
#    Copyright (C) 2015 Comunitea All Rights Reserved
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


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    categ_id = fields.Many2one(default=False)
    wildcard_product = fields.Boolean("Wildcard")

    @api.onchange('categ_id')
    def change_categ_id(self):
        self.sale_delay = self.categ_id.sale_delay

    def action_view_stock_moves(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id.product_tmpl_id', 'in', self.ids)]
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.onchange('categ_id')
    def change_categ_id(self):
        self.sale_delay = self.categ_id.sale_delay

    def action_view_stock_moves(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id', '=', self.id)]
        return action


class ProductCategory(models.Model):
    _inherit = 'product.category'

    sale_delay = fields.Integer('Default sale delay', default=20)
    use_in_sub = fields.Boolean('Use delay in subcategories')

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if vals.get('use_in_sub', False):
            for categ in self:
                if categ.child_id:
                    categ.child_id.write({'sale_delay': categ.sale_delay,
                                          'use_in_sub': True})
        return res
