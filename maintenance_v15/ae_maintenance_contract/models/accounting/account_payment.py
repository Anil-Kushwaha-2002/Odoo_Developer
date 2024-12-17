# -*- coding: utf-8 -*-
from odoo import api, fields, models ,_


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    maintenance_contract_id = fields.Many2one('maintenance.contract')
