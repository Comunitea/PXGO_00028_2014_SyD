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
from datetime import datetime


class stock_pack_operation(models.Model):

    _inherit = 'stock.pack.operation'

    replacement_for_id = fields.Many2one('stock.production.lot',
                                         'Replacement for')


class stock_production_lot(models.Model):

    _inherit = 'stock.production.lot'

    replacement_sended = fields.One2many('stock.pack.operation',
                                         'replacement_for_id',
                                         'Replacements sended')


class stock_transfer_details_item(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    replacement_for_id = fields.Many2one('stock.production.lot',
                                         'Replacement for')
    filter_lots = fields.Many2many('stock.production.lot',
                                   'transfer_details_lot_rel', 'transfer_id',
                                   'lot_id', 'filter lots',
                                   compute='_get_lots')
    picking_type = fields.Char('Picking type', related='transfer_id.picking_id.picking_type_code')

    @api.one
    @api.depends('product_id')
    def _get_lots(self):
        self.filter_lots = self.env['stock.production.lot'].search(
            [('product_id', 'in',
              [x.id for x in self.product_id.replacement_for_ids])])


class stock_transfer_details(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.one
    def do_detailed_transfer(self):
        processed_ids = []
        # Create new and update existing pack operations
        for lstits in [self.item_ids, self.packop_ids]:
            for prod in lstits:
                pack_datas = {
                    'product_id': prod.product_id.id,
                    'product_uom_id': prod.product_uom_id.id,
                    'product_qty': prod.quantity,
                    'package_id': prod.package_id.id,
                    'lot_id': prod.lot_id.id,
                    'location_id': prod.sourceloc_id.id,
                    'location_dest_id': prod.destinationloc_id.id,
                    'result_package_id': prod.result_package_id.id,
                    'date': prod.date if prod.date else datetime.now(),
                    'owner_id': prod.owner_id.id,
                    'replacement_for_id': prod.replacement_for_id.id
                }
                if prod.packop_id:
                    prod.packop_id.write(pack_datas)
                    processed_ids.append(prod.packop_id.id)
                else:
                    pack_datas['picking_id'] = self.picking_id.id
                    packop_id = self.env['stock.pack.operation'].create(
                        pack_datas)
                    processed_ids.append(packop_id.id)
        # Delete the others
        packops = self.env['stock.pack.operation'].search(
            ['&', ('picking_id', '=', self.picking_id.id), '!',
             ('id', 'in', processed_ids)])
        for packop in packops:
            packop.unlink()

        # Execute the transfer of the picking
        self.picking_id.do_transfer()

        return True
