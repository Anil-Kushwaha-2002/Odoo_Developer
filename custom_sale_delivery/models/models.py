# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_sale_delivery(models.Model):
#     _name = 'custom_sale_delivery.custom_sale_delivery'
#     _description = 'custom_sale_delivery.custom_sale_delivery'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

