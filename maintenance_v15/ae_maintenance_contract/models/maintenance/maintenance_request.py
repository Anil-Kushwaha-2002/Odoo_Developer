# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from datetime import date
import logging


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    product_count = fields.Float(compute='_get_product_count',readonly=True)
    apply_expense_to_tenant = fields.Boolean()

    field_service_count = fields.Integer(compute='get_field_service_count', store=True)

    supplier_id = fields.Many2one('res.partner')
    customer_id = fields.Many2one('res.partner')
    supplier_tax_id = fields.Many2one('account.tax', domain="[('type_tax_use', '=', 'purchase')]")
    tenant_tax_id = fields.Many2one('account.tax', domain="[('type_tax_use', '=', 'sale')]")

    product_ids = fields.Many2many('product.product', compute='get_expenses_product', store=True)
    maintenance_request_line_ids = fields.One2many('maintenance.request.line', 'maintenance_request_id')
    project_task_ids = fields.One2many('project.task', 'maintenance_request_id')
    move_ids = fields.One2many('account.move', 'maintenance_request_id')
    maintenance_contract_id = fields.Many2one('maintenance.contract')
    show_maintenance_lines = fields.Boolean(related='stage_id.show_maintenance_lines')
    tenant_name = fields.Char(string="Name", compute='_compute_tenant_info')
    tenant_phone = fields.Char(string="Phone", compute='_compute_tenant_info')
    tenant_mobile = fields.Char(string="Mobile", compute='_compute_tenant_info')
    tenant_email = fields.Char(string="Email", compute='_compute_tenant_info')
    partner_id = fields.Many2one('res.users', string='Partner')
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.company,
                                 )
    created_by_id = fields.Many2one('res.partner', 'Created By', compute='_compute_created_by_id')
    contract_id = fields.Many2one('property.contract','Contract Name')
    termination_date = fields.Date()
    priority = fields.Selection([
        ('0','Normal'),('1','Medium'),
        ('2','High Priority'),
        ('3','Emergency Priority')
    ], required=False, traking=True, string='Priority')
    has_close_stage = fields.Boolean(default=False, compute="_compute_has_close_stage")
    is_in_progress_stage = fields.Boolean(default=False)

    sale_order_ids = fields.Many2many('sale.order', compute='get_sale_orders')
    sale_order_count = fields.Integer(string='Sale orders Count', compute='get_sale_order_count')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    is_excluded = fields.Boolean(string="Excluded")
    email_cc = fields.Char(string="CC Email", compute='_compute_maintenance_contract')
    email_sent = fields.Boolean(string="Email Sent", default=False)
    mt_email_sent = fields.Boolean(string="Email Sent", default=False)


    @api.depends('maintenance_contract_id', 'maintenance_contract_id.partner_id.email', 'maintenance_contract_id.partner_id')
    def _compute_maintenance_contract(self):
        if self.maintenance_contract_id and self.maintenance_contract_id.partner_id:
            self.email_cc = self.maintenance_contract_id.partner_id.email
        else:
            self.email_cc = False

    def action_send_email_oe(self):
        for res in self:
            if res.email_sent:
                raise UserError('Email has already been sent for this maintenance request.')

            # Fetch the email template ID
            template_id = self.env['ir.model.data']._xmlid_to_res_id(
                'ae_maintenance_contract.maintenance_email_notification_template_oe', raise_if_not_found=False)
            email_template_obj = self.env['mail.template'].sudo().browse(template_id)

            if template_id:
                recipient_email = res.email_cc

                # Generate email values
                values = email_template_obj.with_context(
                    active_id=res.id,
                    active_model='maintenance.request'
                ).generate_email(res.id, fields=[
                    'subject', 'body_html', 'email_from', 'email_to'
                ])

                # Set the email recipient
                values['email_to'] = recipient_email or 'default_email@example.com'

                values['body_html'] = (
                    'Maintenance request has been created: {}.<br/><br/>'
                    'Ticket Id: {}<br/>'
                    'Building: {}<br/>'
                    'Flat: {}<br/>'
                    'Request Date: {}<br/><br/>'
                ).format(
                    res.name,
                    res.maintenance_sequence if res.maintenance_sequence else 'N/A',
                    res.building_id.name if res.building_id else 'N/A',
                    res.flat_id.name if res.flat_id else 'N/A',
                    res.request_date.strftime('%Y-%m-%d') if res.request_date else 'N/A',
                )

                out_goin = self.env['ir.mail_server'].sudo().search([], limit=1)

                # Create and send the email
                mail_mail_obj = self.env['mail.mail'].sudo().create(values)
                mail_mail_obj.sudo().send()

                # Mark the email as sent
                res.email_sent = True

    def action_send_under_mt_email_oe(self):
        for res in self:
            if res.mt_email_sent:
                raise UserError('Email has already been sent for this maintenance request.')

            # Fetch the email template ID
            template_id = self.env['ir.model.data']._xmlid_to_res_id(
                'ae_maintenance_contract.maintenance_email_notification_under_mt_template_oe', raise_if_not_found=False)
            email_template_obj = self.env['mail.template'].sudo().browse(template_id)

            if template_id:
                recipient_email = res.company_id.email

                # Generate email values
                values = email_template_obj.with_context(
                    active_id=res.id,
                    active_model='maintenance.request'
                ).generate_email(res.id, fields=[
                    'subject', 'body_html', 'email_from', 'email_to'
                ])

                # Set the email recipient
                values['email_to'] = recipient_email or 'default_email@example.com'

                values['body_html'] = (
                    'Maintenance request has been Under MT: {}.<br/><br/>'
                    'Ticket Id: {}<br/>'
                    'Building: {}<br/>'
                    'Flat: {}<br/>'
                    'Request Date: {}<br/><br/>'
                ).format(
                    res.name,
                    res.maintenance_sequence if res.maintenance_sequence else 'N/A',
                    res.building_id.name if res.building_id else 'N/A',
                    res.flat_id.name if res.flat_id else 'N/A',
                    res.request_date.strftime('%Y-%m-%d') if res.request_date else 'N/A',
                )

                out_goin = self.env['ir.mail_server'].sudo().search([], limit=1)

                # Create and send the email
                mail_mail_obj = self.env['mail.mail'].sudo().create(values)
                mail_mail_obj.sudo().send()

                # Mark the email as sent
                res.mt_email_sent = True


    def action_show_invoice(self):
        return {
            'name': _('Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.invoice_id.id)],
        }

    def action_open_related_sale_orders(self):
        return {
            'name': _('Sale Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.sale_order_ids.ids)],
        }

    def get_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_ids)

    @api.depends('project_task_ids')
    def get_sale_orders(self):
        for rec in self:
            sale_orders = self.env['sale.order']
            for task in rec.project_task_ids:
                if task.sale_order_id:
                    sale_orders += task.sale_order_id
            rec.sale_order_ids = sale_orders.ids
    @api.onchange('stage_id')
    def _onchnage_stage_id_pro(self):

        stage = self.env['maintenance.stage'].search([('name', '=', 'In Progress')], limit=1)
        for rec in self:
            if rec.stage_id == stage:
                rec.is_in_progress_stage = True
            else:
                rec.is_in_progress_stage = False



    @api.depends('stage_id')
    def _compute_has_close_stage(self):
        closed_stage = self.env['maintenance.stage'].search([('name', '=', 'Closed')], limit=1)
        for record in self:
            if record.stage_id == closed_stage:
                record.has_close_stage = True
            else:
                record.has_close_stage = False




    @api.depends('create_uid')
    def _compute_created_by_id(self):
        for record in self:
            record.created_by_id = record.create_uid.partner_id

    @api.onchange('apply_expense_to_tenant')
    def onchange_apply_expense_to_tenant(self):
        tenant = self.env['res.partner'].sudo().search([
            ('name', '=', self.tenant_name)
        ], limit=1)
        self.customer_id = tenant.id if tenant else False

    def _compute_tenant_info(self):
        for rec in self:
            if self.flat_id and self.flat_id.tenant_history_ids:
                filtered_history_ids = self.flat_id.tenant_history_ids.filtered(
                    lambda l: l.date_from <= rec.request_date and (
                            not l.date_to or l.date_to >= rec.request_date
                    )
                )

                last_tenant_record = max(filtered_history_ids, key=lambda h: h.date_from, default=False)

                if last_tenant_record:
                    rec.tenant_name = last_tenant_record.partner_id.name
                    rec.tenant_phone = last_tenant_record.partner_id.phone
                    rec.tenant_mobile = last_tenant_record.partner_id.mobile
                    rec.tenant_email = last_tenant_record.partner_id.email
                else:
                    rec.tenant_name = False
                    rec.tenant_phone = False
                    rec.tenant_mobile = False
                    rec.tenant_email = False
            else:
                rec.tenant_name = False
                rec.tenant_phone = False
                rec.tenant_mobile = False
                rec.tenant_email = False

    def send_email_on_stage_change(self, old_stage, new_stage):
        if old_stage != new_stage and new_stage.trigger_email:
            template = self.env.ref('ae_maintenance_contract.email_template_maintenance_request_stage')
            template.send_mail(self.id, force_send=True)

    def write(self, values):
        old_stage = self._origin.stage_id
        res = super(MaintenanceRequest, self).write(values)
        if 'stage_id' in values:
            new_stage = self.env['maintenance.stage'].browse(values['stage_id'])
            self.filtered(lambda m: m.stage_id.trigger_email).send_email_on_stage_change(old_stage, new_stage)

        return res


    @api.depends('project_task_ids')
    def get_field_service_count(self):
        for rec in self:
            rec.field_service_count = len(rec.project_task_ids)

    @api.depends('maintenance_request_line_ids')
    def get_expenses_product(self):
        for rec in self:
            rec.product_ids = False
            product_ids = []
            for line in rec.maintenance_request_line_ids:
                product_ids.append(line.product_id.id)
            rec.product_ids = product_ids

    @api.depends('product_ids', 'maintenance_request_line_ids')
    def _get_product_count(self):
        for rec in self:
            rec.product_count = len(rec.product_ids)

    def action_create_field_service(self):
        partner_model = self.env['res.partner']
        partner = partner_model.with_user(SUPERUSER_ID).search([('name', '=', self.tenant_name)], limit=1)

        values = {
            'maintenance_request_id': self.id,
            'company_warehouse_id': self.env.company.default_warehouse_id.id or False,
            'name': self.name,
            'flat_name': self.flat_id.name,
            'building_name': self.building_id.name,
            'building_id': self.building_id.id,
            # 'technician_name': self.technician_id.name,
            'planned_date_begin': self.schedule_date,
            'keys_handover': self.keys_handover,
            'priority_sel': self.priority,
            'maintenance_request_type_id': self.maintenance_request_type_id.id if self.maintenance_request_type_id else "",
            'sub_type_id': self.sub_type_id.id if self.sub_type_id else "",
            'location': self.location.id if self.location else "",
            'maintenance_sequence': self.maintenance_sequence if self.maintenance_sequence else "",
            'tenant_name': self.tenant_name,
            'tenant_phone': self.tenant_phone,
            'tenant_mobile': self.tenant_mobile,
            'tenant_email': self.tenant_email,
            'contract_id': self.maintenance_contract_id.id if self.maintenance_contract_id else "",
            'project_preferred_datetime': self.preferred_datetime,
            'project_main_team_id': self.maintenance_team_id.id if self.maintenance_team_id else False,
            'is_no_invoice':  True,
        }

        # if partner:
        #     values['partner_id'] = partner.id

        if self.env.company.default_partner_id:
            values['partner_id'] = self.env.company.default_partner_id.id

        user_id = self.user_id.id
        if user_id:
            values['user_ids'] = [(4, user_id)]
            values['project_user_id'] = user_id

        return self.env['project.task'].with_user(SUPERUSER_ID).create(values)



        # if project_task_id:
        #     return {
        #         'name': _('Project task'),
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'project.task',
        #         'view_mode': 'form',
        #         'res_id': project_task_id.id,
        #         'target': 'current',
        #     }

    @api.model
    def create(self, vals):
        res = super(MaintenanceRequest, self).create(vals)
        for rec in res:
            rec.action_create_field_service()

        template = self.env.ref('ae_maintenance_contract.maintenance_request_email_notification__oe')
        template.send_mail(res.id, force_send=True)
        return res

    def action_open_related_field_service(self):
        project_task_ids = self.project_task_ids.ids if self.project_task_ids else []
        return {
            'name': _('Project task'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', project_task_ids)],
            'context': {
                'default_maintenance_request_id': self.id,
                'default_name': self.name,
            },
            'target': 'current',
        }

    def action_open_related_product(self):
        product_ids = self.product_ids.ids if self.product_ids else []
        return {
            'name': _('Products'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', product_ids)],
            'target': 'current',
        }

    def action_create_expense(self):
        invoice_line_ids = []

        if not self.building_id:
            raise UserError(_("Please set building in maintenance request"))

        if not self.building_id.expense_account_id:
            raise UserError(_("Please set expense account inside building profile"))

        if not self.supplier_id:
            raise UserError(_("Please set supplier"))

        for line in self.maintenance_request_line_ids:
            analytic_account_id = self.flat_id.analytic_account_id.id if (
                    self.flat_id and self.flat_id.analytic_account_id) else False
            if not analytic_account_id and self.building_id:
                analytic_account_id = self.building_id.analytic_account_id.id if (
                        self.building_id and self.building_id.analytic_account_id) else False

            invoice_line_ids.append(
                (0, 0, {
                    "account_id": self.building_id.expense_account_id.id,
                    "name": self.name,
                    "quantity": 1,
                    "analytic_account_id": analytic_account_id,
                    "analytic_tag_ids": [self.building_id.analytic_tag_id.id] if (
                            self.building_id.analytic_tag_id and not self.flat_id) else [],
                    "price_unit": line.price_unit,
                    "tax_ids": [self.supplier_tax_id.id] if self.supplier_tax_id else False,
                })
            )
        if invoice_line_ids:
            move = self.env['account.move'].create({
                "partner_id": self.supplier_id.id,
                'maintenance_request_id': self.id,
                "move_type": "in_invoice",
                "auto_post": True,
                "invoice_date": date.today(),
                "invoice_line_ids": invoice_line_ids
            })
            move.action_post()

        # if self.apply_expense_to_tenant:
        #     self.action_create_customer_invoice()

    def action_create_customer_invoice(self):
        invoice_line_ids = []

        if not self.customer_id:
            raise UserError(_("Please set customer"))

        for line in self.maintenance_request_line_ids:
            analytic_account_id = self.flat_id.analytic_account_id.id if (
                    self.flat_id and self.flat_id.analytic_account_id) else False
            if not analytic_account_id and self.building_id:
                analytic_account_id = self.building_id.analytic_account_id.id if (
                        self.building_id and self.building_id.analytic_account_id) else False
            invoice_line_ids.append(
                (0, 0, {
                    "account_id": self.building_id.other_income_account_id.id,
                    "name": self.name,
                    "quantity": 1,
                    "analytic_account_id": analytic_account_id,
                    "analytic_tag_ids": [self.building_id.analytic_tag_id.id] if (
                            self.building_id.analytic_tag_id and not self.flat_id) else [],
                    "price_unit": line.price_unit,
                    "tax_ids": [self.tenant_tax_id.id] if self.tenant_tax_id else False,
                })
            )
        if invoice_line_ids:
            move = self.env['account.move'].create({
                "partner_id": self.customer_id.id,
                'maintenance_request_id': self.id,
                "ref": self.name,
                "move_type": "out_invoice",
                "auto_post": True,
                "invoice_date": date.today(),
                "invoice_line_ids": invoice_line_ids
            })
            move.action_post()


class MaintenanceRequestLine(models.Model):
    _name = 'maintenance.request.line'
    _description = 'Maintenance Request line'

    quantity = fields.Float(default=1)
    price_unit = fields.Float()
    sub_total = fields.Float(compute='get_sub_total')
    description = fields.Char()
    product_id = fields.Many2one('product.product')
    maintenance_request_id = fields.Many2one('maintenance.request')

    @api.depends('quantity', 'price_unit')
    def get_sub_total(self):
        for rec in self:
            rec.sub_total = rec.price_unit * rec.quantity

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.display_name
            self.price_unit = self.product_id.lst_price
