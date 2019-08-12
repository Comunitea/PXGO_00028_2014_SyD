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
from odoo import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    replacement_for_ids = fields.One2many('product.replacement',
                                          'product_id',
                                          'Replacements for')
    replacement_ids = fields.Many2many(
        'product.replacement',
        'product_replacement_rel',
        'product_id',
        'replacement_id',
        'Replacements')


class ProductReplacement(models.Model):

    _name = 'product.replacement'

    product_id = fields.Many2one('product.product', 'Replacement')
    replacement_for_ids = fields.Many2many(
        'product.product',
        'product_replacement_rel',
        'replacement_id',
        'product_id',
        'Replacement for')
    qty = fields.Float('Quantity')
    disassembly_ref = fields.Char('Disassembly reference')
