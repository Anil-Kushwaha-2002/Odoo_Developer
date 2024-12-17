from odoo import fields, models, api
from lxml import etree


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjectTask, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
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


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjectTaskType, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductTemplate, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
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


class ProjectTags(models.Model):
    _inherit = 'project.tags'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjectTags, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
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

