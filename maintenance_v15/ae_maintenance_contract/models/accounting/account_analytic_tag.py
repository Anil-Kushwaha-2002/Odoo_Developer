# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountAnalyticTag(models.Model):
    _inherit = 'account.analytic.tag'

    building_id = fields.Many2one('project.building', compute='get_related_building')

    def get_related_building(self):
        for rec in self:
            building_id = self.env['project.building'].search([('analytic_tag_id', '=', rec.id)], limit=1)
            rec.building_id = building_id.id if building_id else False

    def action_compute_analytic_distribution(self):
        if self.building_id:
            analytic_distribution_ids = []
            flat_ids = self.env['property.flat'].search([('building_id', '=', self.building_id.id)])
            total_area = 0.0
            for flat in flat_ids:
                total_area += flat.area

            total_percentage = 0.0
            if total_area > 0.0:
                for flat in flat_ids:
                    total_percentage += (flat.area * 100) / total_area
                    analytic_distribution_ids.append((0, 0, {
                        'area': flat.area,
                        'account_id': flat.analytic_account_id.id if flat.analytic_account_id else False,
                        'percentage': (flat.area * 100) / total_area
                    }))

            self.analytic_distribution_ids.unlink()
            self.analytic_distribution_ids = analytic_distribution_ids


class AccountAnalyticDistribution(models.Model):
    _inherit = 'account.analytic.distribution'

    area = fields.Float()
