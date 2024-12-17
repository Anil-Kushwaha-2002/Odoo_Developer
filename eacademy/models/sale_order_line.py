# from odoo import fields, models, api
#
# class SaleOrderLineInherit(models.Model):
#     _inherit = 'sale.order.line'
#
#     name = fields.Char(string='Name', required=True)
#     description = fields.Text(string='Description')
#
#     die_number_id = fields.Char(string="Die Number")
#     diameter = fields.Char(string="Diameter", index=True)
#
#     height = fields.Integer(string="Height", index=True)
#     weight = fields.Float(string="Weight", store=True, digits=(3, 1))
#     complexity = fields.Selection(selection=[("a", "A"), ("b", "B")], string="Complexity")
#
#     def _prepare_invoice_line(self, **optional_values):
#         invoice_line = super()._prepare_invoice_line(**optional_values)
#         invoice_line.update(
#             {   # "die_number_id": self.die_number_id,
#                 # "diameter": self.diameter,
#                 "height": self.height,
#                 "weight": self.weight,
#                 "complexity": self.complexity,
#             })
#         return invoice_line
#
# class AccountMoveLineInherit(models.Model):
#     _inherit = 'account.move.line'
#
#     height = fields.Integer(string="Height")
#     weight = fields.Float(string="Weight (KG)", digits=(3, 1))
#     complexity = fields.Selection([("a", "A"), ("b", "B")], string="Complexity")
#
#




