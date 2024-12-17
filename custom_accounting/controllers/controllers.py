# -*- coding: utf-8 -*-
# from odoo import http


# class CustomAccounting(http.Controller):
#     @http.route('/custom_accounting/custom_accounting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_accounting/custom_accounting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_accounting.listing', {
#             'root': '/custom_accounting/custom_accounting',
#             'objects': http.request.env['custom_accounting.custom_accounting'].search([]),
#         })

#     @http.route('/custom_accounting/custom_accounting/objects/<model("custom_accounting.custom_accounting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_accounting.object', {
#             'object': obj
#         })

