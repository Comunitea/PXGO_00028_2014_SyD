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
    'name': "Prospective customer",
    'version': '11.0.0.0.0',
    'category': '',
    'description': """Adds prospective customers menu and search it
        on sale order, and crm views""",
    'author': 'Comunitea',
    'website': 'www.comunitea.com',
    'depends': ["base",
                "sale",
                "crm",
                "crm_phonecall",
                "sale_crm"],
    'data': ["views/res_partner_view.xml",
             "views/sale_order_view.xml",
             "views/crm_view.xml",
             "views/calendar_view.xml"],
    'installable': True
}
