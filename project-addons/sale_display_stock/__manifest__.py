##############################################################################
#
#    Copyright (C) 2014 Comunitea All Rights Reserved
#    $Omar Castiñeira Saaveda$ <omar@comunitea.com>
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
    "name": "Sale display stock",
    "version": "11.0.0.0.0",
    "author": "Comunitea",
    'website': 'www.comunitea.com',
    "category": "Sales",
    "description": """
Sales display stock
========================================

    * Displays the real stock of product at each sale order line.
""",
    "depends": ["sale_stock"],
    "data": ["views/sale_view.xml"],
    'auto_install': False,
    "installable": True,
}
