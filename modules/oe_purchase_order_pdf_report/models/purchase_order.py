from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_note = fields.Char(string="Note")
    aaqib = fields.Char(string="Purcher")
    mode = fields.Many2one("shipment.mode", string="Mode Of Shipment")
    deliver_term = fields.Char(string="Delivery Terms")
    method_payment = fields.Many2one("account.payment.method", string="Payment Methods")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            record.partner_ref = record.partner_id.ref if record.partner_id.ref else ''

