from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # Call the super method to maintain the original behavior
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            # Automatically create and validate the delivery order
            pickings = order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
            for picking in pickings:
                # Confirm and validate the delivery order
                picking.action_confirm()

                # Calculate 50% quantity for each move line
                for move_line in picking.move_line_ids:
                    if 'qty_done' in move_line._fields:
                        # Calculate 50% of the initial quantity of the move associated with the move line
                        move_line.qty_done = move_line.product_uom_qty * 0.5  # Correct field reference here

                # Validate the picking
                picking.button_validate()

        return res
