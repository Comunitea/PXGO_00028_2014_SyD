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

{
    'name': 'Product replacement',
    'version': '11.0.0.0.0',
    'category': 'product',
    'description': """""",
    'author': 'Comunitea',
    'website': '',
    "depends": ['product', 'stock', 'sale'],
    "data": ['views/product_product_view.xml', 'views/stock_view.xml',
             'wizard/sale_replacement.xml', 'views/sale_view.xml',
             'security/ir.model.access.csv'],
    "installable": True
}
