# -*- coding: utf-8 -*-
import pdb

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError



class ProjectTask(models.Model):
    _inherit = 'project.task'

    maintenance_request_id = fields.Many2one('maintenance.request')
    flat_name = fields.Char('Flat',readonly=True)
    building_name = fields.Char('Building',readonly=True)
    building_id = fields.Many2one('project.building', string='Building')
    property_project_id = fields.Many2one("property.project", required=False)
    income_account_id = fields.Many2one(related='building_id.income_account_id')
    expense_account_id = fields.Many2one(related='building_id.expense_account_id')
    technician_name = fields.Char('Technician')
    keys_handover = fields.Date(string='Keys Handover')
    is_maintenance_type = fields.Boolean(default=False, compute='_compute_is_maintenance_type')
    duration = fields.Float(help="Duration in hours.")
    is_no_invoice = fields.Boolean(string="No invoice")
    priority_sel = fields.Selection([
        ('0', 'Normal'), ('1', 'Medium'),
        ('2', 'High Priority'),
        ('3', 'Emergency Priority')
    ], readonly=True, string='Priority')
    maintenance_request_type_id = fields.Many2one('maintenance.request.type',string='Request type', readonly=True)
    sub_type_id = fields.Many2one('maintenance.request.type', string="Sub Type", readonly=True)
    location = fields.Many2one('maintenance.request.location', string="Location", readonly=True)
    maintenance_sequence = fields.Char(string="Ticket ID", readonly=True)
    tenant_name = fields.Char(string="Name", readonly=True)
    tenant_phone = fields.Char(string="Phone", readonly=True)
    tenant_mobile = fields.Char(string="Mobile", readonly=True)
    tenant_email = fields.Char(string="Email", readonly=True)
    maintenance_type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive'),('move_out_process', 'Move Out Process'),('move_in_process', 'Move In Process')],
                                        compute='_compute_maintenance_type',readonly=True, store=True)

    hide_sale_option = fields.Boolean()
    company_ids = fields.Many2many('res.company', string='Companies',compute='_compute_companies_ids')
    hide_product_sale = fields.Boolean(default=False,compute='_compute_hide_product_sale')
    contract_id = fields.Many2one('maintenance.contract', string="Contract", readonly=True)
    project_preferred_datetime = fields.Datetime(string='Preferred Date-Time')
    timesheet_entry_id = fields.Many2one('account.move', string='Timesheet Entry')
    stock_requisition_ids = fields.One2many('stock.picking', 'maintenance_task_id', string='Stock Requisitions')
    stock_requisition_count = fields.Integer(string='Stock Requisition', compute='get_stock_requisition_count')
    timesheet_hours = fields.Float(string='Time Hours')
    current_company_id = fields.Many2one('res.company', compute="_compute_current_company_id", default=lambda self: self.env.company.id)
    maintenance_contract_generats = fields.Selection([
        ('bills', 'Bills'),
        ('invoice', 'Invoice'),
    ], compute="_compute_current_company_id")

    def action_fsm_view_material_selected_only(self):
        if not self.partner_id:
            raise UserError(_('A customer should be set on the task to generate a worksheet.'))

        self = self.with_company(self.sale_order_company_id)

        domain = [('sale_ok', '=', True),
            '|', ('detailed_type', 'in', ['consu', 'product']),
            '&', '&', ('detailed_type', '=', 'service'), ('invoice_policy', '=', 'delivery'), ('service_type', '=', 'manual'),
            '|', ('company_id', '=', self.sale_order_company_id.id), ('company_id', '=', False)]
        if self.project_id and self.timesheet_product_id:
            domain = expression.AND([domain, [('id', '!=', self.timesheet_product_id.id)]])
        deposit_product = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id')
        if deposit_product:
            domain = expression.AND([domain, [('id', '!=', deposit_product)]])

        domain = expression.AND([domain, [('id', 'in', self.sale_order_id.order_line.mapped('product_id').mapped('id'))]])

        kanban_view = self.env.ref('industry_fsm_sale.view_product_product_kanban_material')
        search_view = self.env.ref('industry_fsm_sale.product_search_form_view_inherit_fsm_sale')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choose Products'),
            'res_model': 'product.product',
            'views': [(kanban_view.id, 'kanban'), (False, 'form')],
            'search_view_id': [search_view.id, 'search'],
            'domain': domain,
            'context': {
                'fsm_mode': True,
                'create': self.env['product.template'].check_access_rights('create', raise_exception=False),
                'fsm_task_id': self.id,  # avoid 'default_' context key as we are going to create SOL with this context
                'pricelist': self.partner_id.property_product_pricelist.id,
                'hide_qty_buttons': self.sale_order_id.sudo().state == 'done',
                'default_invoice_policy': 'delivery',
            },
            'help': _("""<p class="o_view_nocontent_smiling_face">
                            Create a new product
                        </p><p>
                            You must define a product for everything you sell or purchase,
                            whether it's a storable product, a consumable or a service.
                        </p>""")
        }

    def _compute_current_company_id(self):
        for rec in self:
            rec.current_company_id = self.env.company.id
            rec.maintenance_contract_generats = self.env.company.maintenance_contract_generats

    asc_contract_id = fields.Many2one('maintenance.contract', 'ASCC Contract')

    show_product_btn = fields.Boolean(compute='_compute_show_product_btn', store=False)

    def _compute_show_product_btn(self):
        setting_value = self.env['ir.config_parameter'].sudo().get_param('ae_maintenance_contract.show_product_btn',
                                                                         default=False)
        for record in self:
            record.show_product_btn = setting_value


    @api.depends('timesheet_ids.unit_amount')
    def _compute_effective_hours(self):
        res = super(ProjectTask, self)._compute_effective_hours()
        for rec in self:
            if rec.maintenance_request_id:
                rec.effective_hours = rec.timesheet_hours
            else:
                return res
        # if not any(self._ids):
        #     for task in self:
        #         task.effective_hours = sum(task.timesheet_ids.mapped('unit_amount'))
        #     return
        # timesheet_read_group = self.env['account.analytic.line'].read_group([('task_id', 'in', self.ids)],
        #                                                                     ['unit_amount', 'task_id'], ['task_id'])
        # timesheets_per_task = {res['task_id'][0]: res['unit_amount'] for res in timesheet_read_group}
        # for task in self:
        #     task.effective_hours = timesheets_per_task.get(task.id, 0.0)

    def action_open_stock_requisitions(self):
        form = self.env.ref('ae_maintenance_contract.view_picking_formstock_requisition')
        tree = self.env.ref('ae_maintenance_contract.vpicktree_stock_requisition')
        return {
            'name': _('Stock Requisition'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'views': [(tree.id, 'list'), (form.id, 'form')],
            'domain': [('id', 'in', self.stock_requisition_ids.ids)],
        }

    def get_stock_requisition_count(self):
        for rec in self:
            rec.stock_requisition_count = len(rec.stock_requisition_ids)

    def action_create_stock_requisition(self):
        picking_type_id = self.env['stock.picking.type'].search([('warehouse_id', '=', self.company_warehouse_id.id),
                                                                 ('is_maintenance_picking', '=', True)], limit=1)
        form = self.env.ref('ae_maintenance_contract.view_picking_formstock_requisition')
        requisition_stage = self.env['project.task.type'].search([('project_ids', '=', self.project_id.id),
                                              ('stock_requisition_stage', '=', True)], limit=1)
        if requisition_stage:
            self.stage_id = requisition_stage.id
        return {
            'name': _('Create Stock Requisition'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'views': [(form.id, 'form')],
            'view_id': form.id,
            'target': 'current',
            'context': {
                'default_maintenance_task_id': self.id,
                'default_is_stock_requisition': True,
                'default_picking_type_id': picking_type_id.id if picking_type_id else False,
            },
        }


    def action_create_time_sheet_order(self):

        for rec in self:
            product_template_id = self.env['product.template'].search([('is_timesheet_product', '=', True)], limit=1)
            if not product_template_id:
                raise UserError(_("There is no product in the system which have Timesheet Product = 'True'."))
            timesheet_total = 0
            for ts in rec.timesheet_ids:
                if ts.employee_id:
                    timesheet_total += ts.unit_amount * ts.employee_id.timesheet_cost

            # if rec.sale_order_id:
            #     raise ValidationError(_("The record already has an associated Sale Order: %s") % rec.sale_order_id.name)

            if rec.sale_order_id:
                if not any(rec.sale_order_id.order_line.filtered(lambda b: b.product_id.id == product_template_id.product_variant_id.id)):

                    rec.sale_order_id.order_line = [
                        (0, 0, {
                            'name': product_template_id.name,
                            'product_id': product_template_id.product_variant_id.id,
                            'product_uom_qty': 1.0,
                            'product_uom': product_template_id.uom_id.id,
                            'price_unit': timesheet_total
                        }),
                    ]

                return {
                    'name': _('Timesheet Sale Order'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'sale.order',
                    'view_mode': 'tree,form',
                    'domain': [('id', '=', rec.sale_order_id.id)],
                }

            else:
                so_vals = {
                    'partner_id': rec.partner_id.id,
                    'task_id': rec.id,
                    'order_line': [
                        (0, 0, {
                            'name': product_template_id.name,
                            'product_id': product_template_id.product_variant_id.id,
                            'product_uom_qty': 1.0,
                            'product_uom': product_template_id.uom_id.id,
                            'price_unit': timesheet_total
                        }),
                    ],
                    'company_id': self.env.company.id,
                }
                sale_order = self.env['sale.order'].with_user(1).create(so_vals)

                if sale_order:
                    rec.sale_order_id = sale_order.id

                    return {
                        'name': _('Timesheet Sale Order'),
                        'type': 'ir.actions.act_window',
                        'res_model': 'sale.order',
                        'view_mode': 'tree,form',
                        'domain': [('id', '=', sale_order.id)],
                    }


    def show_timesheet_entry_record(self):
        return {
            'name': _('Timesheet Entry'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.timesheet_entry_id.id)],
        }

    def _compute_companies_ids(self):
        allowed_company_ids = self._context.get('allowed_company_ids')
        selected_companies = self.env['res.company'].browse(allowed_company_ids)
        self.company_ids = selected_companies
        return selected_companies

    @api.depends('company_ids.hide_product_sale')
    def _compute_hide_product_sale(self):
        for rec in self:
            hide_product_sale_value = rec.company_ids.mapped('hide_product_sale')
            rec.hide_product_sale = any(hide_product_sale_value)




    @api.depends('maintenance_request_id')
    def _compute_maintenance_type(self):
        for rec in self:
            if rec.maintenance_request_id:
                rec.maintenance_type = rec.maintenance_request_id.maintenance_type
            else:
                rec.maintenance_type = False

    @api.depends('maintenance_request_id')
    def _compute_is_maintenance_type(self):
        for rec in self:
            if rec.maintenance_request_id:
                type = rec.maintenance_request_id.maintenance_type
                if type in ['move_out_process', 'move_in_process']:
                    rec.is_maintenance_type = True
                else:
                    rec.is_maintenance_type = False
            else:
                rec.is_maintenance_type = False


    def _default_partner_id(self):
        return self.env['project.project'].search([('name', '=', 'Field Service')], limit=1).id

    project_id = fields.Many2one(
        'project.project', 'Project', default=_default_partner_id)

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        if (self.stage_id and self.stage_id.maintenance_request_done) and self.maintenance_request_id:
            maintenance_stage_id = self.env['maintenance.stage'].search([('maintenance_request_done', '=', True)], limit=1)
            if maintenance_stage_id:
                self.maintenance_request_id.stage_id = maintenance_stage_id.id
                self.maintenance_request_id.is_in_progress_stage = False

            self.stage_id = self.stage_id.id
        if (self.stage_id and self.stage_id.maintenance_request_received) and self.maintenance_request_id:
            maintenance_stage_id = self.env['maintenance.stage'].search([('maintenance_request_received', '=', True)], limit=1)
            if maintenance_stage_id:
                self.maintenance_request_id.stage_id = maintenance_stage_id.id
                self.maintenance_request_id.is_in_progress_stage = False

            self.stage_id = self.stage_id.id
        if (self.stage_id and self.stage_id.maintenance_request_in_pro) and self.maintenance_request_id:
            maintenance_stage_id = self.env['maintenance.stage'].search([('maintenance_request_in_pro', '=', True)], limit=1)
            if maintenance_stage_id:
                self.maintenance_request_id.stage_id = maintenance_stage_id.id
                self.maintenance_request_id.is_in_progress_stage = True

            self.stage_id = self.stage_id.id

    def action_open_maintenance_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance Request',
            'view_mode': 'form',
            'res_model': 'maintenance.request',
            'res_id': self.maintenance_request_id.id,
            'target': 'current',
        }

    def write(self, vals):
        # Check if the stage_id is being changed and if the task is in 'Stock Requisition' stage
        # for record in self:
        #     if record.stage_id.name == 'Stock Requistion':
        #         if 'stage_id' in vals:
        #             raise UserError(
        #                 "You cannot change the stage when the task is in the 'Stock Requisition' stage.")

        res = super(ProjectTask, self).write(vals)

        if 'timesheet_hours' in vals:
            for task in self:
                if task.sale_order_id:
                    timesheet_line = task.sale_order_id.order_line.filtered(
                        lambda line: line.product_id.is_timesheet_product)
                    if timesheet_line:
                        timesheet_total = 0
                        for ts in task.timesheet_ids:
                            if ts.employee_id:
                                timesheet_total += ts.unit_amount * ts.employee_id.timesheet_cost
                        if timesheet_line:
                            timesheet_line.write({
                                'product_uom_qty': task.timesheet_hours,
                                'price_unit': timesheet_total / task.timesheet_hours if task.timesheet_hours > 0 else timesheet_total
                            })

        # If the stage_id was changed, update related maintenance request stages
        if 'stage_id' in vals:
            for task in self:
                if task.maintenance_request_id:
                    if task.stage_id.name in ['Closed', 'In Progress', 'Stock Requistion']:
                        stage_record = self.env['maintenance.stage'].search(
                            [('name', '=', task.stage_id.name)], limit=1)
                        if stage_record:
                            task.maintenance_request_id.stage_id = stage_record.id
        return res

    @api.onchange('timesheet_hours')
    def _onchange_timesheet_hours(self):
        for task in self:
            timesheet_lines = task.timesheet_ids
            if timesheet_lines:
                for line in timesheet_lines:
                    whole_hours = int(task.timesheet_hours)
                    fractional_hours = task.timesheet_hours - whole_hours

                    # Convert fractional part to minutes and then back to decimal
                    minutes = fractional_hours * 60
                    correct_hours = whole_hours + (minutes / 60.0)

                    line.unit_amount = correct_hours

    @api.onchange('planned_date_begin','planned_date_end')
    def _onchange_planned_date_begin(self):
        for task in self:
            timesheet_lines = task.timesheet_ids
            if timesheet_lines:
                if not task.stage_id.name in ['Planned']:
                    stage_record = self.env['project.task.type'].search(
                        [('name', '=', 'Planned')], limit=1)
                    if stage_record:
                        task.stage_id = stage_record.id
                for line in timesheet_lines:
                    line.date = task.planned_date_begin

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    maintenance_request_done = fields.Boolean()
    maintenance_request_in_pro = fields.Boolean()
    stock_requisition_stage = fields.Boolean(string='Stock Requisition Stage')
    maintenance_request_received = fields.Boolean()


class ResCompany(models.Model):
    _inherit = 'res.company'

    hide_product_sale = fields.Boolean(default=False)
    is_default_company = fields.Boolean(default=False, string='Show As Default Company')
    maintenance_contract_generats = fields.Selection([
        ('bills', 'Bills'),
        ('invoice', 'Invoice'),
    ], default='bills', string="Maintenance Contract Generates")
    default_warehouse_id = fields.Many2one('stock.warehouse', string="Task: Warehouse")
    default_partner_id = fields.Many2one('res.partner', string="Task: Customer")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_product_btn = fields.Boolean('Show Product Button?')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            show_product_btn=self.env['ir.config_parameter'].sudo().get_param(
                'ae_maintenance_contract.show_product_btn', default=False)
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('ae_maintenance_contract.show_product_btn',
                                                         self.show_product_btn)



