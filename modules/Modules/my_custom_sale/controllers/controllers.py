# -*- coding: utf-8 -*-
# from odoo import http


# class MyCustomSale(http.Controller):
#     @http.route('/my_custom_sale/my_custom_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_custom_sale/my_custom_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_custom_sale.listing', {
#             'root': '/my_custom_sale/my_custom_sale',
#             'objects': http.request.env['my_custom_sale.my_custom_sale'].search([]),
#         })

#     @http.route('/my_custom_sale/my_custom_sale/objects/<model("my_custom_sale.my_custom_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_custom_sale.object', {
#             'object': obj
#         })

