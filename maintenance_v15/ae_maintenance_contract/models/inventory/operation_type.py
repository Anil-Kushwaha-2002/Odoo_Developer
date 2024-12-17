
from odoo import models, api, fields, _
from odoo.exceptions import UserError
from odoo.osv import expression
from datetime import datetime, time ,timedelta
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.picking.type'

    is_maintenance_picking = fields.Boolean(string="Maintenance Picking Type")
