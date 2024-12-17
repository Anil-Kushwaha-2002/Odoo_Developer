# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSaleDelivery(http.Controller):
#     @http.route('/custom_sale_delivery/custom_sale_delivery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sale_delivery/custom_sale_delivery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sale_delivery.listing', {
#             'root': '/custom_sale_delivery/custom_sale_delivery',
#             'objects': http.request.env['custom_sale_delivery.custom_sale_delivery'].search([]),
#         })

#     @http.route('/custom_sale_delivery/custom_sale_delivery/objects/<model("custom_sale_delivery.custom_sale_delivery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sale_delivery.object', {
#             'object': obj
#         })

