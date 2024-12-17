from odoo import fields, models, api
class seal_order_inherit(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    payment_type = fields.Char(string='Payment_type')
    description = fields.Text(string='Description')
    start_date = fields.Date(string="Start Date")