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

{
    'name': "SyD customizations",
    'version': '1.0',
    'category': '',
    'description': """""",
    'author': 'Pexego',
    'website': '',
    "depends": ['product', 'stock', 'purchase', 'product_sequence',
    #TODO: Migrar'product_pack',
                'account_due_list', 'sale_stock', 'warning',
                'crm_phonecall'],
    "data": ['product_view.xml', 'purchase_view.xml', 'account_view.xml',
             'stock_view.xml', 'data/ir_sequence.xml',
             'wizard/sale_order_update_purchase_price.xml', 'sale_view.xml',
             'data/res_partner_title_data.xml'],
    "installable": True
}
