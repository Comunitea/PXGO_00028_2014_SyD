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

{
    'name': "Document customizations",
    'version': '11.0.0.0.0',
    'category': '',
    'description': """""",
    'author': 'Comunitea',
    'website': '',
    "depends": ['sale', 'stock', 'sale_stock', 'picking_services',
                'delivery', 'supplier_ref', 'account_payment_mode',
                'mrp_bom_phantom_fix', 'syd_custom', 'purchase_discount',
                'account_invoice_production_lot',
                'stock_picking_report_valued',
                'report_qweb_element_page_visibility', 'sale_margin',
                'account_invoice_report_due_list',
                'account_invoice_report_grouped_by_picking'],

    "data": ['views/sale_view.xml',
             'views/stock_view.xml', 'views/purchase_order.xml',
             'qweb_report/report_saleorder.xml',
             'qweb_report/report_stockpicking.xml',
             'qweb_report/report_purchase_order.xml',
             'qweb_report/report_header.xml', 'qweb_report/report_invoice.xml',
             'sale_report.xml', 'stock_report.xml', 'account_report.xml'],
    "installable": True
}
