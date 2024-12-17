from odoo import models, api, exceptions

class SaleAutomation(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super(SaleAutomation, self).action_confirm()

        for sale_rec in self:
            try:
                delivery = self.env['stock.picking'].search(
                    [('sale_id', '=', sale_rec.id), ('state', 'not in', ['done', 'cancel'])]
                )

                if delivery:
                    delivery.action_assign()

                    # Reduce move quantities by 50% within a try-except block
                    for move in delivery.move_ids_without_package:
                        try:
                            move.quantity = move.product_uom_qty * 0.5
                        except (ValueError, TypeError):
                            # Handle specific exceptions for quantity modification
                            message = f"Invalid quantity for move {move.id}. Expected numerical value."
                            raise exceptions.UserError(message)

                    delivery.with_context(skip_backorder=True).button_validate()

                    if delivery.backorder_id:
                        backorder = delivery.backorder_id
                        backorder.action_assign()
                        backorder.button_validate()
            except exceptions.ValidationError as e:
                # Catch validation errors from delivery confirmation
                message = f"Delivery confirmation failed for sale order {sale_rec.id}: {e}"
                raise exceptions.UserError(message)
            except exceptions.Warning as e:
                # Catch warnings for potential issues (optional)
                message = f"Delivery confirmation for sale order {sale_rec.id} encountered warnings: {e}"
                self.env.user.notify(message, title="Delivery Warning")

        return True








# from odoo import models, fields, api
# from odoo.exceptions import UserError
#
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     @api.model
#     def action_confirm(self):
#         res = super(SaleOrder, self).action_confirm()
#
#         for order in self:
#             if not order.picking_ids:
#                 raise UserError("No delivery orders found for this sale order.")
#
#             picking = order.picking_ids[0]
#
#             # Create two delivery orders: one for 50% and one for the remaining 50%
#             picking_1 = picking.copy()
#             picking_2 = picking.copy()
#
#             # Process 50% of the quantities for the first delivery order
#             for move_line in picking_1.move_line_ids:
#                 qty_done = move_line.product_uom_qty * 0.5
#                 move_line.quantity_done = qty_done
#                 move_line.write({'quantity_done': qty_done})
#             # Confirm the first delivery order
#             picking_1.with_context({'no_backorder': True}).button_validate()
#
#             # Process the remaining 50% for the second delivery order
#             for move_line in picking_2.move_line_ids:
#                 qty_done = move_line.product_uom_qty * 0.5
#                 move_line.quantity_done = qty_done
#                 move_line.write({'quantity_done': qty_done})
#             # Assign stock for the second delivery order but don't validate
#
#             picking_2.action_assign()
#
#         return res