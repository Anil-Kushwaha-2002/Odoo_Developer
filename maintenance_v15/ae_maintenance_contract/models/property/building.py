# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PropertyProject(models.Model):
    _inherit = 'property.project'

    project_task_ids = fields.One2many('project.task', 'property_project_id', string="Tasks")
    m_contract_ids = fields.Many2many('maintenance.contract', compute="_compute_m_contract_ids")
    deferred_revenue_id = fields.Many2one(
        comodel_name='account.account',
        string="Deferred Revenue", domain=lambda x: [('company_id', '=', x.env.company.id)])

    def _compute_m_contract_ids(self):
        for rec in self:
            rec.m_contract_ids = False
            if rec.project_task_ids:
                rec.m_contract_ids = [(6, 0, rec.project_task_ids.mapped('contract_id').ids)]

    def action_open_project_tasks(self):
        return {
            'name': _('Project Tasks'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.project_task_ids.ids)],
            'context': {
                'create': False,
            },
            'target': 'current',
        }

    def action_open_maintenance_contracts(self):
        return {
            'name': _('Maintenance contract'),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.contract',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.m_contract_ids.ids)],
            'context': {
                'create': False,
            },
            'target': 'current',
        }


class Building(models.Model):
    _inherit = 'project.building'

    maintenance_contract_count = fields.Integer(compute='get_maintenance_contact_info')

    analytic_tag_id = fields.Many2one('account.analytic.tag')
    maintenance_contract_ids = fields.Many2many('maintenance.contract', compute='get_maintenance_contact_info')

    def get_maintenance_contact_info(self):
        for rec in self:
            rec.maintenance_contract_ids = False
            rec.maintenance_contract_count = 0.0
            maintenance_contract_ids = self.env['maintenance.contract'].search([('building_ids', 'in', rec.id)])
            if maintenance_contract_ids:
                rec.maintenance_contract_ids = maintenance_contract_ids.ids
                rec.maintenance_contract_count = len(maintenance_contract_ids)

    def action_related_maintenance_contract(self):
        maintenance_contract_ids = self.maintenance_contract_ids.ids if self.maintenance_contract_ids else []
        return {
            'name': _('Maintenance contract'),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.contract',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', maintenance_contract_ids)],
            'context': {
                'default_building_id': self.id,
            },
            'target': 'current',
        }
