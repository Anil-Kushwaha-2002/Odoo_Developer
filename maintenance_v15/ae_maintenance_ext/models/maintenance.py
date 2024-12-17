# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    """Client requirement to change it to M2M from M2O"""
    technician_user_id = fields.Many2many('res.users', string='Responsibles', tracking=True, default=lambda self: [(4, self.env.uid)])


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id.technician_user_id:
            self.technician_user_id = self.category_id.technician_user_id[0].id


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    @api.onchange('category_id')
    def onchange_category_id(self):
        if not self.user_id or not self.equipment_id or (self.user_id and not self.equipment_id.technician_user_id):
            if self.category_id.technician_user_id:
                self.user_id = self.category_id.technician_user_id[0]