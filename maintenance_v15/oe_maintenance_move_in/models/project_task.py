# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class ProjectTask(models.Model):
    _inherit = 'project.task'
    is_maintenance_type =fields.Boolean(default=False)



    def action_move_in_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/maintenance/report/' + str(self.id),
        }


