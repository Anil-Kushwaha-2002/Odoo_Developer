# -*- coding: utf-8 -*-
import pdb

from odoo import models, fields, api, _


class StockMove(models.Model):
    _inherit = "stock.move"

    maintenance_task_id = fields.Many2one('project.task', string="Maintenance Task", compute='get_maintenance_task_id', store=True)
    maintenance_sequence = fields.Char(related='maintenance_task_id.maintenance_sequence', string="Ticket ID",
                                       readonly=True, store=True)
    building_id = fields.Many2one(related='maintenance_task_id.building_id', string='Building', store=True)
    property_project_id = fields.Many2one(related='maintenance_task_id.property_project_id', string='Project')
    maintenance_request_type_id = fields.Many2one(related='maintenance_task_id.maintenance_request_type_id',
                                                  string='Request type', readonly=True, store=True)
    maintenance_type = fields.Selection(related='maintenance_task_id.maintenance_type', readonly=True, store=True)
    source_location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        compute='_compute_source_location_id',
        store=True,
    )

    matching_building_id = fields.Many2one(
        comodel_name='project.building',
        string='Building'
    )

    @api.depends('picking_id')
    def _compute_source_location_id(self):
        for move in self:
            if move.picking_id:
                move.source_location_id = move.picking_id.location_id
            else:
                move.source_location_id = False

    destination_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        compute='_compute_destination_location_id',
        store=True,
    )

    @api.depends('matching_building_id')
    def _compute_destination_location_id(self):
        for move in self:
            if move.matching_building_id:
                move.destination_location_id = move.matching_building_id.destination_location_id
            else:
                move.destination_location_id = False

    @api.depends('picking_id', 'picking_id.maintenance_task_id')
    def get_maintenance_task_id(self):
        for rec in self:
            if rec.picking_id and rec.picking_id.maintenance_task_id:
                rec.maintenance_task_id = rec.picking_id.maintenance_task_id.id
            else:
                rec.maintenance_task_id = False

    # @api.model
    # def create(self, vals):
    #     res = super(StockMove, self).create(vals)
    #     for rec in res:
    #         if rec.sale_line_id and rec.picking_id and not rec.picking_id.maintenance_task_id:
    #             if rec.sale_line_id.order_id.task_id:
    #                 rec.picking_id.maintenance_task_id = rec.sale_line_id.order_id.task_id.id
    #     return rec
