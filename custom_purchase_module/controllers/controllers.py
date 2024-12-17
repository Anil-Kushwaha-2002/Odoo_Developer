# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPurchaseModule(http.Controller):
#     @http.route('/custom_purchase_module/custom_purchase_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_purchase_module/custom_purchase_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_purchase_module.listing', {
#             'root': '/custom_purchase_module/custom_purchase_module',
#             'objects': http.request.env['custom_purchase_module.custom_purchase_module'].search([]),
#         })

#     @http.route('/custom_purchase_module/custom_purchase_module/objects/<model("custom_purchase_module.custom_purchase_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_purchase_module.object', {
#             'object': obj
#         })

