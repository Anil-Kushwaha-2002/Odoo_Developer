# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date


class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    maintenance_request_done = fields.Boolean()
    show_maintenance_lines = fields.Boolean()
    trigger_email = fields.Boolean()
    maintenance_request_in_pro = fields.Boolean()
    maintenance_request_received = fields.Boolean()

