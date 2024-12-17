from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"
    _description = "Inherited Res Company"

    commercial = fields.Char(string="For Commercial", store=True)
    technical = fields.Char(string="For Technical", store=True)
    delivery = fields.Char(string="For Delivery", store=True)
    manager = fields.Many2one("hr.employee", string="Supply Chain Manager", store=True)




