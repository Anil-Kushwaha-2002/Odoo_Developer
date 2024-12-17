from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_contract_company = fields.Boolean(string="Contracting Company")
