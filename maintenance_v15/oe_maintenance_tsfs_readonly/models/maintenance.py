from odoo import fields, models, api
from lxml import etree


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MaintenanceRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'kanban':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//kanban"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res


class MaintenanceContract(models.Model):
    _inherit = 'maintenance.contract'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MaintenanceContract, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MaintenanceEquipment, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'kanban':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//kanban"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res


class MaintenanceTeam(models.Model):
    _inherit = 'maintenance.team'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MaintenanceTeam, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res

class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MaintenanceEquipmentCategory, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res

class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MaintenanceStage, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res


class MaintenanceRequstType(models.Model):
    _inherit = 'maintenance.request.type'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MaintenanceRequstType, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res

class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MailActivityType, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if self.env.user.has_group('oe_maintenance_tsfs_readonly.maintenance_timesheet_fieldservice_readonly') and self.env.company.is_contract_company:
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//tree"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//form"):
                    node.set('create', "0")
                    node.set('edit', "0")
                    res['arch'] = etree.tostring(doc)
        return res
