# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import pandas as pd
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class MaintenanceContract(models.Model):
    _name = 'maintenance.contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Maintenance contract'

    maintenance_contract_generats = fields.Selection([
        ('bills', 'Bills'),
        ('invoice', 'Invoice'),
    ], compute="_compute_maintenance_contract_generats", default=lambda self: self.env.company.maintenance_contract_generats)

    def _compute_maintenance_contract_generats(self):
        for rec in self:
            rec.maintenance_contract_generats = self.env.company.maintenance_contract_generats
    active = fields.Boolean(default=True)
    name = fields.Char(compute='get_contract_name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('running', 'Running'),
        # ('to_renew', 'To Be Renew'),
        # ('force_renew', 'Force Renew'),
        # ('expired', 'Expired'),
        ('closed', 'Closed'),
        ('cancel', 'Cancelled'),
    ], copy=False, index=True, tracking=True, default='draft')

    date_from = fields.Date()
    date_to = fields.Date()
    installment_no = fields.Integer(default=1)
    recurring_period_installment = fields.Integer(default=1)
    pay_with_check = fields.Boolean()
    untaxed_amount = fields.Float()
    taxed_amount = fields.Float(compute='get_taxed_amount')
    payment_count = fields.Integer(compute='_get_payment_count')
    check_count = fields.Integer(compute='_get_check_count')
    maintenance_count = fields.Integer(compute='_get_maintenance_count')

    building_id = fields.Many2one('project.building')
    building_ids = fields.Many2many('project.building')
    building_maintenance_ids = fields.One2many('project.building.maintenance', 'maintenance_contract_id')
    analytic_tag_ids = fields.Many2many('account.analytic.tag')
    bank_id = fields.Many2one('res.bank')

    installment_lines = fields.One2many("maintenance.installment.line", "contract_id", copy=False)
    maintenance_type_ids = fields.Many2many("maintenance.request.type")
    maintenance_request_ids = fields.One2many('maintenance.request', 'maintenance_contract_id')
    bill_ids = fields.One2many('account.move', 'maintenance_contract_id')
    payment_ids = fields.One2many('account.payment', 'maintenance_contract_id', copy=False)
    check_ids = fields.One2many("pdc.wizard", "maintenance_contract_id", copy=False)
    move_line_ids = fields.Many2many('account.move.line')
    tax_id = fields.Many2one(comodel_name="account.tax",
                             domain="[('company_id', '=', company_id), ('type_tax_use', '=', 'purchase')]")
    journal_id = fields.Many2one("account.journal", domain=[('type', 'in', ['cash', 'bank'])])
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner')
    closed_date = fields.Date(string="Closed Date", readonly=1)
    preventive = fields.Integer(string="Preventive")
    maintenance_team_id = fields.Many2one("maintenance.team",string="Team")
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    is_active_start = fields.Boolean('Generate From Start', default=False)
    is_fixed_preventive = fields.Boolean(default=False)
    months_of_repetition = fields.Integer('Months of repetition')
    day_to_start = fields.Integer('Day of Start')
    is_generate = fields.Boolean(default=False, compute='_compute_is_generate')
    maintenance_request_type = fields.Selection(
        [('corrective', 'Corrective'), ('preventive', 'Preventive'), ('move_out_process', 'Move Out Process'),
         ('move_in_process', 'Move In Process')], string='Maintenance Type')


    # def action_open_related_maintenance_request(self):
    #     return {
    #         'name': _('Maintenance Request'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'maintenance.request',
    #         'view_mode': 'tree,form',
    #         'domain': [('maintenance_contract_id', '=', self.name)],
    #         'target': 'current',
    #     }

    def _compute_is_generate(self):
        for record in self:
            related_requests = self.env['maintenance.request'].search(
                [('maintenance_contract_id', '=', record.id), ('maintenance_type', '=', 'preventive')])
            record.is_generate = bool(related_requests)


    @api.constrains('date_from', 'date_to', 'partner_id', 'maintenance_type_ids', 'building_maintenance_ids', 'state')
    def check_no_repeat(self):
        if self.date_from and self.date_to:
            self.check_convergence()

    def check_convergence(self):
        history = self.search([('id', 'not in', self.ids), ('partner_id', '=', self.partner_id.id),
                               ('partner_id', '=', self.partner_id.id), ('state', '=', 'running')])
        for rec in history:
            if any(x.id in rec.maintenance_type_ids.ids for x in self.maintenance_type_ids) and any(
                    x.id in rec.building_ids.ids for x in self.building_ids):
                ranges = pd.date_range(self.date_from, self.date_to, freq='d')
                if rec.date_from in [r.date() for r in ranges] or rec.date_to in [r.date() for r in ranges]:
                    raise exceptions.ValidationError(
                        "You can't create more than one running maintenance contract on same supplier,Maintenance types,Buildings\n this maintenance contracts already exist:{}".format(
                            rec.name))

    @api.onchange('building_maintenance_ids')
    def _onchange_building_maintenance(self):
        building_maintenance_ids = self.building_maintenance_ids

        # Get analytic tags
        self.analytic_tag_ids = False
        analytic_tag_ids = []
        for line in building_maintenance_ids.mapped('building_id'):
            if line.analytic_tag_id:
                analytic_tag_ids.append(line.analytic_tag_id._origin.id)

        self.analytic_tag_ids = analytic_tag_ids

        # Get buildings from "building_maintenance_ids"
        self.building_ids = False
        self.building_ids = building_maintenance_ids.mapped('building_id').ids if building_maintenance_ids else []

        # Compute maintenance contract untaxed
        self.untaxed_amount = sum(building_maintenance_ids.mapped('untaxed_amount'))

    @api.depends('payment_ids')
    def _get_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    @api.depends('check_ids')
    def _get_check_count(self):
        for rec in self:
            rec.check_count = len(rec.check_ids)

    @api.depends('maintenance_request_ids')
    def _get_maintenance_count(self):
        for rec in self:
            rec.maintenance_count = len(rec.maintenance_request_ids)


    @api.depends('tax_id', 'untaxed_amount')
    def get_taxed_amount(self):
        for rec in self:
            rec.taxed_amount = 0.0
            if rec.tax_id:
                taxes = rec.tax_id.compute_all(rec.untaxed_amount)
                if taxes:
                    rec.taxed_amount = taxes['total_included']
            else:
                rec.taxed_amount = rec.untaxed_amount

    @api.depends('partner_id', 'date_from', 'date_to')
    def get_contract_name(self):
        for rec in self:
            rec.name = 'Contract For ' + str(rec.partner_id.name or '') + ' - ' + str(
                rec.date_from or '') + ' : ' + str(rec.date_to or '')

    def action_compute_installment(self):
        for rec in self:
            if rec.installment_no:
                installment_amount = rec.untaxed_amount / rec.installment_no
                installment_list = []
                date = rec.date_from
                for line in range(0, rec.installment_no):
                    installment_list.append((0, 0, {'date': date,
                                                    'untaxed_amount': installment_amount,
                                                    'journal_id': rec.journal_id.id if rec.journal_id else False,
                                                    'tax_id': rec.tax_id.id if rec.tax_id else False,
                                                    }))
                    date = date + relativedelta(months=rec.recurring_period_installment)
                rec.installment_lines = False
                rec.installment_lines = installment_list


    def action_send_notification(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data._xmlid_lookup('ae_maintenance_contract.notification_mail_template')[2]

        except ValueError:
            template_id = False

        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
        except ValueError:
            compose_form_id = False

        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'maintenance.contract',
            'active_model': 'maintenance.contract',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
            'default_partner_ids': [self.partner_id.id]

        })
        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_lang([ctx['default_res_id']])[ctx['default_res_id']]

        self = self.with_context(lang=lang)
        if self.state in ['draft']:
            ctx['model_description'] = _('Start Renewal case')

        # Send Legal to "mail.compose.message" as default value
        ctx['default_contract_id'] = self.id


        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }








    def action_payment_checks(self):
        # Create supplier payments ber installment
        self.create_installment_payments()

    def action_confirm(self):
        if not self.installment_lines:
            raise UserError(_("Please compute installment first."))

        if self.check_ids:
            if any(not c.reference for c in self.check_ids):
                raise exceptions.ValidationError(_('Set Check Reference on each check first'))

        contracts = self.env['maintenance.contract'].search(
            [('id', '!=', self.id), ('building_ids', 'in', self.building_ids.ids),
             ('state', 'in', ['confirm', 'running'])])
        # Check duplicate contracts
        # for cont in contracts:
        #     if cont.date_to >= self.date_from >= cont.date_from and self.maintenance_type_ids.ids == cont.maintenance_type_ids.ids:
        #         raise exceptions.ValidationError(_('This building has a contract running or confirmed in the period'))

        # Change contract state
        if self.date_from <= date.today() <= self.date_to:
            self.state = 'running'
        else:
            self.state = 'confirm'

        # Create supplier bill
        if self.env.company.maintenance_contract_generats == 'bills':
            self.create_supplier_bill()
        if self.env.company.maintenance_contract_generats == 'invoice':
            self.create_customer_invoice()

    def create_customer_invoice(self):
        for rec in self:
            if rec.installment_no:
                date = rec.date_from
                for line in range(0, rec.installment_no):
                    invoice_line_ids = []
                    for building in rec.building_maintenance_ids:
                        invoice_line_ids.append((0, 0, {
                            "account_id": building.building_id.income_account_id.id,
                            # Use income account for customer invoices
                            "name": rec.name,
                            "quantity": 1,
                            # You can uncomment the analytic lines if needed
                            # "analytic_account_id": building.building_id.analytic_account_id.id if building.building_id.analytic_account_id else False,
                            # "analytic_tag_ids": [
                            #     building.building_id.analytic_tag_id.id] if building.building_id.analytic_tag_id else [],
                            "price_unit": building.untaxed_amount / rec.installment_no,  # Divide price by installment
                            "tax_ids": [(6, 0, [rec.tax_id.id])] if rec.tax_id else False,
                        }))

                    # Create the invoice move for each installment
                    move = self.env['account.move'].create({
                        "partner_id": rec.partner_id.id,
                        'maintenance_contract_id': rec.id,
                        "move_type": "out_invoice",
                        "auto_post": True,
                        "invoice_date": date,
                        "invoice_date_due": date,
                        "invoice_line_ids": invoice_line_ids
                    })

                    # Move to the next installment date
                    date = date + relativedelta(months=rec.recurring_period_installment)

    def create_supplier_bill(self):
        for rec in self:
            if rec.installment_no:
                date = rec.date_from
                for line in range(0, rec.installment_no):
                    invoice_line_ids = []
                    for building in self.building_maintenance_ids:
                        invoice_line_ids.append((0, 0, {
                            "account_id": building.building_id.expense_account_id.id,
                            "name": self.name,
                            "quantity": 1,
                            # "analytic_account_id": building.building_id.analytic_account_id.id if building.building_id.analytic_account_id else False,
                            "analytic_tag_ids": [
                                building.building_id.analytic_tag_id.id] if building.building_id.analytic_tag_id else [],
                            "price_unit": building.untaxed_amount / rec.installment_no,
                            "tax_ids": [self.tax_id.id] if self.tax_id else False,
                        }))
                    move = self.env['account.move'].create({
                        "partner_id": self.partner_id.id,
                        'maintenance_contract_id': self.id,
                        "move_type": "in_invoice",
                        "auto_post": True,
                        "invoice_date": date,
                        "invoice_date_due": date,
                        "invoice_line_ids": invoice_line_ids
                    })
                    date = date + relativedelta(months=rec.recurring_period_installment)

    def create_installment_payments(self):
        payment_list = []
        for line in self.installment_lines:
            if not self.pay_with_check:
                payment_list.append({
                    'date': line.date,
                    'amount': line.taxed_amount,
                    'payment_type': 'outbound',
                    'ref': line.ref,
                    'partner_id': self.partner_id.id,
                    'journal_id': line.journal_id.id,
                    'maintenance_contract_id': self.id,
                })
            else:
                payment_list.append({
                    "partner_id": self.partner_id.id,
                    "payment_type": 'send_money',
                    "maintenance_contract_id": self.id,
                    "payment_date": fields.date.today(),  # Replace [line.date] with [current date]
                    "due_date": line.date,
                    "bank_id": self.bank_id.id,
                    "journal_id": line.journal_id.id,
                    "memo": 'Maintenance Contract ' + str(self.name),
                    "payment_amount": line.taxed_amount,
                    "invoice_ids": self.bill_ids.ids if self.bill_ids else [],
                })

        if self.pay_with_check:
            payments = self.env['pdc.wizard'].create(payment_list)
            for payment in payments:
                payment.sudo().action_state_register()
        else:
            payments = self.env['account.payment'].create(payment_list)
            # Update auto_post of journal entries related to the created payments
            for payment in payments:
                payment.move_id.auto_post = True
                payment.move_id.maintenance_contract_id = False

    def action_open_related_payment(self):
        payment_ids = self.payment_ids.ids if self.payment_ids else []
        return {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', payment_ids)],
            'context': {
                'default_maintenance_contract_id': self.id,
            },
            'target': 'current',
        }

    def action_open_related_equipment(self):
        equipment_ids = []
        for contract in self:
            for building in contract.building_ids:
                equipment_ids += self.env['maintenance.equipment'].search([
                    ('flat_id.building_id', '=', building.id),
                    ('maintenance_type_ids', 'in', contract.maintenance_type_ids.ids)
                ]).filtered(lambda e: all(
                    maintenance_type.id in contract.maintenance_type_ids.ids for maintenance_type in
                    e.maintenance_type_ids)).ids
        return {
            'name': _('Equipment'),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', equipment_ids)],
            'target': 'current',
        }


    def action_open_related_preventive_request(self):


        return {
            'name': _('Preventive Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'view_mode': 'tree,form',
            'domain': [('maintenance_contract_id', '=', self.id),('maintenance_type','=','preventive')],
            'target': 'current',
        }


    def action_generate_requests(self):
        self.ensure_one()
        if self.is_fixed_preventive:
            self.generate_requests_fixed_date()
        elif not self.is_fixed_preventive:
            if self.preventive <= 0 and self.is_fixed_preventive:
                raise ValidationError("Preventive days must be greater than Zero.")

            current_date = self.date_from if self.is_active_start else self.date_from + timedelta(days=self.preventive)
            generated_dates = []

            while current_date < self.date_to:
                generated_dates.append(current_date)
                current_date += timedelta(days=self.preventive)

            if self.is_active_start:
                generated_dates.pop()

            equipment_ids = set()
            for contract in self:
                for building in contract.building_ids:
                    equipment_ids.update(self.env['maintenance.equipment'].search([
                        ('flat_id.building_id', '=', building.id),
                        ('maintenance_type_ids', 'in', contract.maintenance_type_ids.ids)
                    ]).filtered(lambda e: all(
                        maintenance_type.id in contract.maintenance_type_ids.ids for maintenance_type in
                        e.maintenance_type_ids)).ids)

            created_requests = []
            for equipment_id in equipment_ids:
                equipment = self.env['maintenance.equipment'].browse(equipment_id)
                for request_date in generated_dates:
                    request = self.env['maintenance.request'].create({
                        'name': _('Preventive Maintenance - %s' % equipment.name),
                        'request_date': request_date,
                        'schedule_date': request_date,
                        'category_id': equipment.category_id.id,
                        'equipment_id': equipment.id,
                        'maintenance_type': 'preventive',
                        'owner_user_id': equipment.owner_user_id.id,
                        'user_id': equipment.technician_user_id.id,
                        'maintenance_team_id': self.maintenance_team_id.id,
                        'duration': equipment.maintenance_duration,
                        'company_id': equipment.company_id.id or self.env.company.id,
                        'building_id': equipment.building_id.id,
                        'flat_id': equipment.flat_id.id,
                        'maintenance_contract_id': self.id,
                    })
                    created_requests.append(request.id)

            return True

    def generate_requests_fixed_date(self):
        self.ensure_one()
        if self.months_of_repetition < 0:
            raise ValidationError("Month of repetition must be greater than Zero")
        if self.day_to_start >31 or self.day_to_start<0:
            raise ValidationError("Day of start must be between 0 and 31")

        current_date = self.date_from if self.is_active_start else self.date_from + relativedelta(months=self.months_of_repetition)
        day_to_start = self.day_to_start

        if day_to_start > 1:
            current_date = current_date.replace(day=day_to_start)
            print("\n\n\\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n",current_date)
            if current_date < self.date_from and self.is_active_start:
                current_date += relativedelta(months=1)

        generated_dates = []

        while current_date < self.date_to:
            generated_dates.append(current_date)
            current_date += relativedelta(months=self.months_of_repetition)
            if current_date < self.date_from:
                continue
            # generated_dates.append(current_date)

        if generated_dates and generated_dates[-1] > self.date_to:
            generated_dates.pop()

        equipment_ids = set()
        for contract in self:
            for building in contract.building_ids:
                equipment_ids.update(self.env['maintenance.equipment'].search([
                    ('flat_id.building_id', '=', building.id),
                    ('maintenance_type_ids', 'in', contract.maintenance_type_ids.ids)
                ]).filtered(lambda e: all(
                    maintenance_type.id in contract.maintenance_type_ids.ids for maintenance_type in
                    e.maintenance_type_ids)).ids)
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nequipment_ids',equipment_ids)

        created_requests = []
        for equipment_id in equipment_ids:
            equipment = self.env['maintenance.equipment'].browse(equipment_id)
            for request_date in generated_dates:
                if request_date > self.date_to:
                    break
                request = self.env['maintenance.request'].create({
                    'name': _('Preventive Maintenance - %s' % equipment.name),
                    'request_date': request_date,
                    'schedule_date': request_date,
                    'category_id': equipment.category_id.id,
                    'equipment_id': equipment.id,
                    'maintenance_type': 'preventive',
                    'owner_user_id': equipment.owner_user_id.id,
                    'user_id': equipment.technician_user_id.id,
                    'maintenance_team_id': self.maintenance_team_id.id,
                    'duration': equipment.maintenance_duration,
                    'company_id': equipment.company_id.id or self.env.company.id,
                    'building_id': equipment.building_id.id,
                    'flat_id': equipment.flat_id.id,
                    'maintenance_contract_id': self.id,
                })
                created_requests.append(request.id)

        return True


    def action_open_related_check(self):
        check_ids = self.check_ids.ids if self.check_ids else []
        return {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'pdc.wizard',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', check_ids)],
            'context': {
                'default_maintenance_contract_id': self.id,
            },
            'target': 'current',
        }

    def action_open_related_maintenance(self):
        maintenance_request_ids = self.maintenance_request_ids.ids if self.maintenance_request_ids else []
        return {
            'name': _('Maintenance request'),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', maintenance_request_ids)],
            'context': {
                'default_maintenance_contract_id': self.id,
                'default_building_id': self.building_ids[0].id if self.building_ids else False,
            },
            'target': 'current',
        }

    def action_check_contract_running(self):
        for rec in self.env['maintenance.contract'].search(
                [('state', 'not in', ['closed', 'cancel', 'running'])]):
            if rec.date_from <= date.today() <= rec.date_to:
                rec.state = 'running'

    def action_cancel(self):
        self.state = 'cancel'
        self.bill_ids.write({'state': 'cancel'})
        self.is_generate = False

    def action_reset_draft(self):

        self.write({'state': 'draft'})
        self = self.with_context(force_delete=True)
        self.bill_ids.unlink()

    def action_close(self):
        return {
            'name': _('Close Maintenance Contract'),
            'type': 'ir.actions.act_window',
            'res_model': 'close.maintenance.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('ae_maintenance_contract.close_maintenance_wizard').id,
            'target': 'new',
            'context': {'default_close_date': fields.Date.today()},
            'flags': {'form': {'action_buttons': True}},
        }

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("You can not delete contract when state not draft"))

        return super(MaintenanceContract, self).unlink()


class MaintenanceInstallmentLine(models.Model):
    _name = 'maintenance.installment.line'
    _rec_name = 'contract_id'
    _description = 'New Description'

    date = fields.Date()
    untaxed_amount = fields.Float()
    taxed_amount = fields.Float(compute='get_taxed_amount')
    ref = fields.Char()

    contract_id = fields.Many2one('maintenance.contract')
    journal_id = fields.Many2one("account.journal", domain=[('type', 'in', ['cash', 'bank'])])
    tax_id = fields.Many2one("account.tax",
                             domain="[('company_id', '=', company_id), ('type_tax_use', '=', 'purchase')]")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    # @api.depends('contract_id', 'date')
    # def get_installment_ref(self):
    #     for rec in self:
    #         rec.ref = (_('Supplier :')) + str(rec.contract_id.partner_id.name) + " , installment of :" + str(rec.date)

    @api.depends('tax_id', 'untaxed_amount')
    def get_taxed_amount(self):
        for rec in self:
            rec.taxed_amount = 0.0
            if rec.tax_id:
                taxes = rec.tax_id.compute_all(rec.untaxed_amount)
                if taxes:
                    rec.taxed_amount = taxes['total_included']
            else:
                rec.taxed_amount = rec.untaxed_amount


class ProjectBuildingMaintenance(models.Model):
    _name = 'project.building.maintenance'
    _rec_name = 'building_id'
    _description = 'Project Building Maintenance'

    untaxed_amount = fields.Float()

    maintenance_contract_id = fields.Many2one('maintenance.contract')
    building_id = fields.Many2one('project.building')
    project_id = fields.Many2one('property.project')
