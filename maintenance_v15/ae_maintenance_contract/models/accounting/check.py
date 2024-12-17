# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Check(models.Model):
    _inherit = 'pdc.wizard'

    maintenance_contract_id = fields.Many2one('maintenance.contract')

