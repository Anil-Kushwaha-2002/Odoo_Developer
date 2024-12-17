import pdb

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from odoo.osv import expression
from datetime import datetime, time ,timedelta
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_stock_requisition = fields.Boolean(string='Stock Requisition')
    maintenance_task_id = fields.Many2one('project.task', string="Maintenance Task")
    maintenance_sequence = fields.Char(related='maintenance_task_id.maintenance_sequence', string="Ticket ID", readonly=True)
    building_id = fields.Many2one(related='maintenance_task_id.building_id', string='Building', store=True)
    flat_name = fields.Char('Flat', related='maintenance_task_id.flat_name', store=True)
    property_project_id = fields.Many2one(related='maintenance_task_id.property_project_id', string='Project')
    maintenance_request_type_id = fields.Many2one(related='maintenance_task_id.maintenance_request_type_id', string='Request type', readonly=True)
    maintenance_type = fields.Selection(related='maintenance_task_id.maintenance_type', readonly=True, store=True)
    have_to_create_requisition = fields.Boolean(string="Have To Create RFQ", compute="get_have_to_create_requisition")
    purchase_requisition_ids = fields.One2many('purchase.order', 'requisition_picking_id',string='Purchase Requisition')
    rfq_count = fields.Integer(string="RFQ's", compute='get_rfq_count')
    delivery_number = fields.Char(string="Delivery Number")
    destination_location_ids = fields.Many2many('stock.location', 'dest_picking_rel', 'picking_id', 'location_id', string="Destination Locations", compute="_compute_destination_location_ids", store=True)


    @api.depends('move_ids_without_package')
    def _compute_destination_location_ids(self):
        for rec in self:
            rec.destination_location_ids = [(6,0,rec.move_ids_without_package.mapped('destination_location_id').ids)]


    def get_rfq_count(self):
        """In this we are computing RFQ count but also we are computing maintenance task id
        which will come from sale_id if any!"""
        for rec in self:
            rec.rfq_count = len(rec.purchase_requisition_ids)

            sale_id = False
            if rec.sale_id:
                sale_id = rec.sale_id
            if not sale_id:
                sale_move_lines = rec.move_lines.filtered(lambda b: b.sale_line_id)
                if sale_move_lines:
                    sale_id = sale_move_lines[0].sale_line_id.order_id
            if sale_id and not rec.maintenance_task_id:
                if sale_id.task_id:
                    rec.maintenance_task_id = sale_id.task_id.id

    def action_create_purchase_requisition(self):
        for rec in self:
            vendor_ids = self.env['res.partner']
            for move in rec.move_lines.filtered(lambda b: b.availability < b.product_uom_qty and b.product_uom_qty != b.reserved_availability):
                if len(move.product_id.seller_ids) < 1:
                    raise ValidationError(_('In Product: %s There is no Vendor Info in Purchase Tab.' % move.product_id.name))
                if move.product_id.seller_ids:

                    if move.product_id.seller_ids[0].name.id not in vendor_ids.ids:
                        vendor_ids += move.product_id.seller_ids[0].name

            for vendor in vendor_ids:

                order_line = []
                for move in rec.move_lines.filtered(lambda b: b.availability < b.product_uom_qty and b.product_uom_qty != b.reserved_availability):
                    if vendor.id == move.product_id.seller_ids[0].name.id:
                        vals = {
                                'name': move.product_id.name,
                                'product_id': move.product_id.id,
                                'product_qty': move.product_uom_qty - move.availability,
                                'product_uom': self.product_id.uom_po_id.id,
                                'price_unit': move.product_id.seller_ids[0].price,
                                'date_planned': datetime.today(),
                                'taxes_id': False,
                            }
                        order_line.append((0, 0, vals))

                purchase_order = self.env['purchase.order'].create({
                    'partner_id': vendor.id,
                    'requisition_picking_id': rec.id,
                    'order_line': order_line,
                })



            if rec.purchase_requisition_ids:
                return {
                    'name': _('Request For Quotation'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'purchase.order',
                    'view_mode': 'tree,form',
                    'domain': [('id', 'in', rec.purchase_requisition_ids.ids)],
                }

    def action_open_request_for_quotation(self):
        if self.purchase_requisition_ids:
            return {
                'name': _('Request For Quotation'),
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.purchase_requisition_ids.ids)],
            }


    def get_have_to_create_requisition(self):
        for rec in self:
           if any(rec.move_lines.filtered(lambda b: b.availability < b.product_uom_qty and b.product_uom_qty != b.reserved_availability)):
               rec.have_to_create_requisition = True
           else:
                rec.have_to_create_requisition = False

    def button_set_fsm_quantity(self):
        for rec in self:
            for move in rec.move_lines:
                print(move.quantity_done, 'quantity_done')
                move.product_id.with_user(1).with_context({'fsm_task_id': rec.maintenance_task_id.id}).with_user(1).set_fsm_quantity(move.quantity_done)

    def button_set_fsm_quantity(self):
        for rec in self:
            for move in rec.move_lines:
                print(move.quantity_done, 'quantity_done')
                move.product_id.with_user(1).with_context({'fsm_task_id': rec.maintenance_task_id.id}).with_user(1).set_fsm_quantity(move.quantity_done)

    def button_validate(self):
        context = dict(self.env.context) or {}
        if self.sale_id:
            context.update({'sale_id': self.sale_id})
        self.env.context = context
        res = super(StockPicking, self.with_user(1).with_context(sale_id=self.sale_id)).button_validate()
        for rec in self:
            for move in rec.move_lines:
                if move.destination_location_id:
                    move.location_dest_id = move.destination_location_id
                for move_line in move.move_line_ids:
                    if move.destination_location_id:
                        move_line.location_dest_id = move.destination_location_id
                print(move.quantity_done, 'quantity_done')
                move.product_id.with_user(1).with_context({'fsm_task_id': rec.maintenance_task_id.id}).with_user(1).set_fsm_quantity(move.quantity_done)
        return res

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def set_fsm_quantity(self, quantity):
        task = self._get_contextual_fsm_task()
        # project user with no sale rights should be able to change material quantities
        if not task or quantity and quantity < 0 or not self.user_has_groups('project.group_project_user'):
            return
        self = self.sudo()

        # don't add material on locked SO
        if task.sale_order_id.sudo().state == 'done':
            return False
        # ensure that the task is linked to a sale order
        task.with_user(1)._fsm_ensure_sale_order()
        wizard_product_lot = self.action_assign_serial()
        if wizard_product_lot:
            return wizard_product_lot
        self.fsm_quantity = quantity
        return True
