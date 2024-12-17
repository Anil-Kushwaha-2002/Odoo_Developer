# -*- coding: utf-8 -*-
import pdb

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    maintenance_contract_id = fields.Many2one('maintenance.contract')
    maintenance_request_id = fields.Many2one('maintenance.request')
    is_combined_contract_invoice = fields.Boolean(string='Is Combined Contract Invoice')



    def _post(self, soft=True):
        """Overide to add value in context to use in _inter_company_create_invoices"""
        for rec in self:
            context = dict(self.env.context) or {}
            context.update({'is_combined_contract_invoice': rec.is_combined_contract_invoice})
            self.env.context = context

        posted = super()._post(soft)
        return posted


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    building_id = fields.Many2one('project.building', string='Building')
    property_project_id = fields.Many2one("property.project")

    def _inter_company_prepare_invoice_line_data(self):
        """Inherited to check the context for is_combined_contract_invoice and then add building account here.
        """
        res = super()._inter_company_prepare_invoice_line_data()
        if 'is_combined_contract_invoice' in self.env.context:
            if self.env.context.get('is_combined_contract_invoice'):
                if self.display_type:
                    res['account_id'] = False
                elif self.property_project_id and self.property_project_id.with_company(self.env.company).income_account_id:
                    res['account_id'] = self.property_project_id.with_company(self.env.company).income_account_id.id

                if self.env.company.maintenance_contract_generats == 'invoice':
                    res['account_id'] = self.building_id.with_company(self.env.company).income_account_id.id
        return res
