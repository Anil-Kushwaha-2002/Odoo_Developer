from odoo import models, fields, api


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    maintenance_task_id = fields.Many2one('project.task', string="Maintenance Task", compute='get_maintenance_task_id',
                                          store=True)
    maintenance_sequence = fields.Char(related='maintenance_task_id.maintenance_sequence', string="Ticket ID",
                                       readonly=True, store=True)
    building_id = fields.Many2one(related='maintenance_task_id.building_id', string='Building', store=True)
    property_project_id = fields.Many2one(related='maintenance_task_id.property_project_id', string='Project', store=True)
    maintenance_request_type_id = fields.Many2one(related='maintenance_task_id.maintenance_request_type_id',
                                                  string='Request type', readonly=True)
    maintenance_type = fields.Selection(related='maintenance_task_id.maintenance_type', readonly=True, store=True)

    @api.depends('stock_move_id')
    def get_maintenance_task_id(self):
        for rec in self:
            if rec.stock_move_id and rec.stock_move_id.maintenance_task_id:
                rec.maintenance_task_id = rec.stock_move_id.maintenance_task_id.id
            else:
                rec.maintenance_task_id = False
