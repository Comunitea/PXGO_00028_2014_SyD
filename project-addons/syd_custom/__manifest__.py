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
    'name': "SyD customizations",
    'version': '11.0.0.0.0',
    'category': '',
    'description': """""",
    'author': 'Comunitea',
    'website': '',
    "depends": ['product', 'stock', 'purchase', 'product_sequence',
                'account_due_list', 'sale_stock', 'crm_phonecall',
                'sale_disable_inventory_check', 'account_payment_order',
                'delivery', 'hide_product_variants', 'sale_order_revision'],
    "data": ['views/product_view.xml', 'views/purchase_view.xml',
             'views/account_view.xml', 'views/stock_view.xml',
             'data/ir_sequence.xml', 'data/syd_custom_data.xml',
             'wizard/sale_order_update_purchase_price.xml',
             'views/sale_view.xml', 'data/res_partner_title_data.xml'],
    "installable": True
}
