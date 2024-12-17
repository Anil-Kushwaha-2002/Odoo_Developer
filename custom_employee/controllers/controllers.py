# -*- coding: utf-8 -*-
# from odoo import http


# class CustomEmployee(http.Controller):
#     @http.route('/custom_employee/custom_employee', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_employee/custom_employee/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_employee.listing', {
#             'root': '/custom_employee/custom_employee',
#             'objects': http.request.env['custom_employee.custom_employee'].search([]),
#         })

#     @http.route('/custom_employee/custom_employee/objects/<model("custom_employee.custom_employee"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_employee.object', {
#             'object': obj
#         })

