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
from openerp import models, fields, api, exceptions, _


class purchase_order(models.Model):

    _inherit = 'purchase.order'

    notes = fields.Text('Terms and Conditions', default="""Deberán enviar especificaciones técnicas de los equipos o materiales ofertados.
Indicarán el precio unitario de cada material de forma detallada y el total de su oferta.
Los precios serán netos, o en su caso se indicará el descuento realizado, e incluirá todos los conceptos como embalajes, estudios, etc.
Se indicarán los portes hasta nuestro local en A Coruña, por separado.
Se indicará el PLAZO DE ENTREGA MÁXIMO.""")
