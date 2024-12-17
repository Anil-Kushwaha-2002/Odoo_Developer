# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Building(models.Model):
    _inherit = 'owner.contract'
    maintenance_bill_ids = fields.Many2many('account.move', compute='get_maintenance_bill_from_building')
    maintenance_entry_id= fields.Many2one('account.move', string='Maintenance Entry')
    building_maintenance_value = fields.Float()

    @api.depends('building_id','building_id.maintenance_contract_ids','building_id.maintenance_contract_ids.bill_ids', 'owner_id')
    def get_maintenance_bill_from_building(self):
        for rec in self:
            rec.maintenance_bill_ids = rec.building_id.maintenance_contract_ids.filtered_domain(
                [('state', 'in', ['confirm', 'running'])]).mapped('bill_ids').filtered_domain(
                [('state', '=', 'posted')]).ids
    # @api.depends('maintenance_bill_ids')
    # def compute_value(self):
    #     for rec in self:
    #         amt = 0
    #         for inv in rec.maintenance_bill_ids:
    #             building_count = len(inv.maintenance_contract_id.building_ids)
    #             if building_count:
    #                 amt += inv.amount_total/building_count
    #
    #         rec.building_maintenance_value = amt
    def create_maintenance_entry(self):
        line_list = []
        line_debit = (0, 0, {
            'name': 'maintenance for owner contract:{}'.format(self.name),
            'account_id': self.owner_id.property_account_payable_id.id,
            'partner_id': self.owner_id.id,
            'debit': self.building_maintenance_percentage,
        })
        line_credit = (0, 0, {
            'name': 'maintenance for owner contract:{}'.format(self.name),
            'account_id': self.building_id.expense_account_id.id,
            'partner_id': self.owner_id.id,
            'credit': self.building_maintenance_percentage,
        })
        line_list.append(line_debit)
        line_list.append(line_credit)
        move = self.env['account.move'].create({'partner_id': self.owner_id.id,
                                                'move_type': 'entry',
                                                'line_ids': line_list,
                                                "date": fields.date.today(),
                                                })
        move.action_post()
        self.write({'maintenance_entry_id': move.id})