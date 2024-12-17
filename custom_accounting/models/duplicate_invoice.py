from odoo import models, api, fields

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    def duplicate_invoice(self):
        current_invoice = self

        # Create a new invoice by duplicating relevant fields
        new_invoice = self.env['account.move'].create({
            'partner_id': current_invoice.partner_id.id,   # Copy customer (partner)
            'move_type': current_invoice.move_type,        # Copy invoice type (e.g., sale, purchase)
            'invoice_date': current_invoice.invoice_date,  # Copy invoice date
            'currency_id': current_invoice.currency_id.id, # Copy currency
            'journal_id': current_invoice.journal_id.id,   # Copy journal
            'invoice_origin': current_invoice.name,        # Set original invoice reference
            'narration': current_invoice.narration,        # Copy internal note

            'invoice_line_ids': [(0, 0, {
                'product_id': line.product_id.id,          # Copy product
                'quantity': line.quantity,                 # Copy quantity
                'price_unit': line.price_unit,             # Copy price
                'account_id': line.account_id.id,          # Copy account
                'tax_ids': [(6, 0, line.tax_ids.ids)],     # Copy applicable taxes
                'name': line.name,                         # Copy description
            }) for line in current_invoice.invoice_line_ids]
        })

        # Post the invoice automatically after creating it
        new_invoice.action_post()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': new_invoice.id,
            'target': 'current',
        }





# # models/account_move_inherit.py
# from odoo import models, api, fields
#
# class AccountMoveInherit(models.Model):
#     _inherit = 'account.move'
#
#     def duplicate_invoice(self):
#         # Get the current invoice (self refers to the active record)
#         current_invoice = self
#
#         # Create a new invoice by duplicating relevant fields
#         new_invoice = self.env['account.move'].create({
#             'partner_id': current_invoice.partner_id.id,   # Copy customer (partner)
#             'move_type': current_invoice.move_type,        # Copy invoice type (e.g., sale, purchase)
#             'invoice_date': current_invoice.invoice_date,  # Copy invoice date
#             'currency_id': current_invoice.currency_id.id, # Copy currency
#             'journal_id': current_invoice.journal_id.id,   # Copy journal
#             'invoice_origin': current_invoice.name,        # Set original invoice reference
#             'narration': current_invoice.narration,        # Copy any internal note
#             # Add other fields you want to copy from the invoice
#         })
#
#         # Duplicate invoice lines
#         for line in current_invoice.invoice_line_ids:
#             new_line = self.env['account.move.line'].create({
#                 'move_id': new_invoice.id,                # Link to the new invoice
#                 'product_id': line.product_id.id,         # Copy product
#                 'quantity': line.quantity,                # Copy quantity
#                 'price_unit': line.price_unit,            # Copy price
#                 'account_id': line.account_id.id,         # Copy account (This is the critical field)
#                 'tax_ids': [(6, 0, line.tax_ids.ids)],    # Copy applicable taxes
#                 'name': line.name,                        # Copy description
#                 # Add other necessary fields
#             })
#
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'account.move',
#             'view_mode': 'form',
#             'res_id': new_invoice.id,
#             'target': 'current',
#         }






# from odoo import models
#
# class AccountMove(models.Model):
#     _inherit = 'account.move'
#
#     def action_duplicate_invoice_sql(self):
#         self.ensure_one()  # Ensure only one record is selected
#
#         # SQL to duplicate the invoice
#         query_invoice = """
#             INSERT INTO account_move (name, partner_id, invoice_date, state, move_type, currency_id, amount_total, amount_untaxed)
#             SELECT name || '_duplicate', partner_id, invoice_date, 'draft', move_type, currency_id, amount_total, amount_untaxed
#             FROM account_move WHERE id = %s
#             RETURNING id
#         """
#         self.env.cr.execute(query_invoice, (self.id,))
#         new_invoice_id = self.env.cr.fetchone()[0]
#
#         # SQL to duplicate move lines
#         query_move_lines = """
#             INSERT INTO account_move_line (move_id, name, account_id, debit, credit, balance, quantity, product_id)
#             SELECT %s, name, account_id, debit, credit, balance, quantity, product_id
#             FROM account_move_line WHERE move_id = %s
#         """
#         self.env.cr.execute(query_move_lines, (new_invoice_id, self.id))
#
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Duplicated Invoice',
#             'view_mode': 'form',
#             'res_model': 'account.move',
#             'res_id': new_invoice_id,
#             'target': 'current',
#         }




