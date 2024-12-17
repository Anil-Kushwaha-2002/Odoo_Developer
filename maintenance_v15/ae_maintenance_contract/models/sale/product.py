# -*- coding: utf-8 -*-
import pdb

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_timesheet_product = fields.Boolean(string='Timesheet Product')

    def _get_product_accounts(self):
        accounts = super(ProductTemplate, self)._get_product_accounts()
        res = self._get_asset_accounts()
        if 'sale_id' in self.env.context:
            if self.env.context.get('sale_id'):
                if self.env.context.get('sale_id').task_id:
                    if self.env.company.maintenance_contract_generats == 'bills':
                        if self.env.context.get('sale_id').task_id.property_project_id:
                            if self.env.context.get('sale_id').task_id.property_project_id.with_company(self.env.company).expense_account_id:
                                accounts.update({
                                    'stock_output': self.env.context.get('sale_id').task_id.property_project_id.with_company(self.env.company).expense_account_id or res['stock_output'],
                                })
                    if self.env.company.maintenance_contract_generats in ['invoice','bills']:
                        if self.env.context.get('sale_id').task_id.building_id:
                            if self.env.context.get('sale_id').task_id.building_id.with_company(self.env.company).expense_account_id:
                                accounts.update({
                                    'stock_output': self.env.context.get('sale_id').task_id.building_id.with_company(self.env.company).expense_account_id or res['stock_output'],
                                })

        return accounts