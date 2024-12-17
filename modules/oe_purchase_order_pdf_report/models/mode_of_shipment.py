from odoo import fields, models


class SteelTypeMaster(models.Model):
    _name = "shipment.mode"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "shipment Mode"

    name = fields.Char(string="Name", store="True")
    mode_shipment = fields.Char(string="Mode of Shipment", tracking=True)
