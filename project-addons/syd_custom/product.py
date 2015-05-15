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

class productTemplate(models.Model):

    _inherit = 'product.template'

    _defaults = {
        'categ_id': False,
        'warranty': 12,
    }

    @api.onchange('categ_id')
    def change_categ_id(self):
        self.sale_delay = self.categ_id.sale_delay

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.onchange('categ_id')
    def change_categ_id(self):
        self.sale_delay = self.categ_id.sale_delay


    @api.multi
    def write(self, vals):
        for product in self:
            new_code = False
            if product.default_code in [False, '/', ''] or ('default_code' in vals and vals['default_code'] == '/'):
                if product.seller_ids:
                    if product.seller_ids[0].name.ref and product.seller_ids[0].product_code:
                        vals['default_code'] = product.seller_ids[0].name.ref + ":" + \
                                               product.seller_ids[0].product_code
                        new_code = True
                if not new_code:
                    vals['default_code'] = self.env['ir.sequence'].get(
                    'product.product')
            super(ProductProduct, product).write(vals)
        return True


class productCategory(models.Model):
    _inherit = 'product.category'

    sale_delay = fields.Integer('Default sale delay', default=20)
    use_in_sub = fields.Boolean('Use delay in subcategories')

    @api.one
    def write(self, vals):
        res = super(productCategory, self).write(vals)
        if vals.get('use_in_sub', False):
            if self.child_id:
                self.child_id.write({'sale_delay': self.sale_delay, 'use_in_sub': True})
        return res
