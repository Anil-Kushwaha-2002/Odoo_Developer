# -*- coding: utf-8 -*-
import pdb

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # building_id = fields.Many2one(related='task_id.building_id', string="Building", store=True)
    property_project_id = fields.Many2one(related='task_id.property_project_id', string="Project", store=True)
    external_building = fields.Boolean(related='task_id.property_project_id.external_building', string='External Owner', store=True)
    building_id = fields.Many2one(related='task_id.building_id', string='Building')
    maintenance_request_type_id = fields.Many2one(related='task_id.maintenance_request_type_id',
                                                  string='Request type', readonly=True)
    maintenance_type = fields.Selection(related='task_id.maintenance_type', readonly=True, store=True)

    invoice_status = fields.Selection(selection_add=[
        ('draft', 'Draft'), ('upselling',),
        ('closed', 'Closed'),
    ], default='draft')
    timesheet_entry_id = fields.Many2one('account.move', string='Timesheet Entry')
    is_invoice = fields.Boolean(string="No invoice", compute='_compute_task')
    timesheet_hours = fields.Float(string='Timesheet Hours', compute='_compute_timesheet_hours')

    @api.depends('task_id.is_no_invoice', 'task_id')
    def _compute_task(self):
        for order in self:
            if order.task_id:
                order.is_invoice = order.task_id.is_no_invoice
            else:
                order.is_invoice = False

    @api.depends('task_id.timesheet_hours', 'task_id')
    def _compute_timesheet_hours(self):
        for order in self:
            if order.task_id:
                order.is_invoice = order.task_id.is_no_invoice
                order.timesheet_hours = sum(order.task_id.mapped('timesheet_hours'))
            else:
                order.timesheet_hours = 0.0

    @api.depends('property_project_id', 'external_building', 'state', 'order_line.invoice_status')
    def _get_invoice_status(self):
        """Handling of a specific situation: an order contains building and external owner is false"""
        super()._get_invoice_status()
        for order in self.filtered(lambda order: order.property_project_id and order.external_building == False):
            order.invoice_status = 'closed'

    def create_maintenance_timesheet_entry(self):
        line_ids = []
        credit_total = 0
        for rec in self:
            if rec.timesheet_entry_id:
                raise ValidationError(_("The already Timesheet Entry Created"))

            order_lines = rec.order_line.filtered(lambda b: b.product_id.product_tmpl_id.is_timesheet_product == True)
            if rec.order_line.filtered(lambda b: b.product_id.product_tmpl_id.is_timesheet_product == True):
                for line in order_lines:
                    if not line.product_id.product_tmpl_id.categ_id.property_stock_valuation_account_id:
                        raise UserError(
                            _("On the 'TimeSheet product Category' there is no Stock Valuation Account selected!"))

                    expense_account_id = rec.building_id.with_company(self.env.company).expense_account_id.id
                    if not expense_account_id:
                        raise UserError(_("The expense account for the building is not set!"))

                    debit_vals = {
                        'name': rec.property_project_id.with_company(self.env.company).expense_account_id.name,
                        'partner_id': rec.partner_id.id,
                        'account_id': expense_account_id,
                        'debit': abs(line.price_subtotal),
                        'credit': 0.0
                    }
                    if self.env.company.maintenance_contract_generats == 'invoice':
                        expense_account_id = rec.building_id.with_company(self.env.company).expense_account_id.id
                        if not expense_account_id:
                            raise UserError(_("The expense account for the building is not set!"))

                        debit_vals['name'] = rec.building_id.with_company(self.env.company).expense_account_id.name
                        debit_vals['account_id'] = expense_account_id
                    line_ids.append((0, 0, debit_vals))
                    credit_total += abs(line.price_subtotal)

                credit_account_id = order_lines[0].product_id.categ_id.property_stock_valuation_account_id.id
                if not credit_account_id:
                    raise UserError(_("The stock valuation account for the product category is not set!"))

                credit_vals = {
                    'name': order_lines[0].product_id.categ_id.property_stock_valuation_account_id.name,
                    'partner_id': rec.partner_id.id,
                    'account_id': credit_account_id,
                    'debit': 0.0,
                    'credit': abs(credit_total),
                }
                line_ids.append((0, 0, credit_vals))

        if line_ids != []:
            journal_types = ['sale']
            journal = self.env['account.move']._search_default_journal(journal_types)

            vals = {
                'ref': rec.name,
                'date': fields.date.today(),
                'partner_id': rec.partner_id.id,
                'journal_id': journal.id,
                'invoice_date_due': fields.date.today(),
                'move_type': 'entry',
                'line_ids': line_ids
            }
            move_id = self.env['account.move'].sudo().with_context(default_journal_id=journal.id).create(vals)
            move_id.action_post()
            if move_id:
                rec.task_id.timesheet_entry_id = move_id.id
                rec.timesheet_entry_id = move_id.id
                return {
                    'name': _('Timesheet Entry'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'view_mode': 'tree,form',
                    'domain': [('id', '=', move_id.id)],
                }

    def show_timesheet_entry_record(self):
        return {
            'name': _('Timesheet Entry'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.timesheet_entry_id.id)],
        }

    def show_timesheet_hour_record(self):
        return {
            'name': _('Timesheet Entry'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.task_id.id)],
        }


    def action_create_sos_invoice(self):
        property_project_ids = self.mapped('task_id').mapped('property_project_id')
        # if not self[0].task_id.maintenance_request_id.invoice_id:

        invoice_line_list = []

        for project in property_project_ids:
            project_income = 0
            project_sale_orders = self.filtered(lambda b: b.task_id.property_project_id.id == project.id)
            project_income = sum(project_sale_orders.mapped('amount_total'))
            vals = {
                'name': project.with_company(self.env.company).income_account_id.name or False,
                'quantity': 1,
                'price_unit': project_income,
                'account_id': project.with_company(self.env.company).income_account_id.id or False,
                'tax_ids': False,
                'property_project_id': project.id,
            }
            invoice_line_list.append((0, 0, vals))

        if len(invoice_line_list) > 0:
            invoice_vals = {
                "date": fields.date.today(),
                "partner_id": self[0].partner_id.id,
                "company_id": self[0].company_id.id,
                "invoice_line_ids": invoice_line_list,
                "is_combined_contract_invoice": True,

            }
            invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_vals)

            if invoice:
                self[0].task_id.maintenance_request_id.invoice_id = invoice.id

            return {
                'name': _('Invoice'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'tree,form',
                'domain': [('id', '=', invoice.id)],
            }

        # else:
        #     raise ValidationError("Invoice is Already Exists in Related Maintenance Request!, Delete the invoice First!")

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if not res.is_invoice:
            res.invoice_status = 'draft'
        if res.is_invoice:
            res.invoice_status = 'no'
        return res

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for record in self:
            if 'state' in vals:
                if record.is_invoice:
                    record.invoice_status = 'no'
                else:
                    record.invoice_status = 'draft'
        return res

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            if record.is_invoice:
                record.invoice_status = 'no'
            else:
                record.invoice_status = 'draft'
        return res
