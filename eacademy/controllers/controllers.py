# -*- coding: utf-8 -*-
# from odoo import http


# class Eacademy(http.Controller):
#     @http.route('/eacademy/eacademy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eacademy/eacademy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eacademy.listing', {
#             'root': '/eacademy/eacademy',
#             'objects': http.request.env['eacademy.eacademy'].search([]),
#         })

#     @http.route('/eacademy/eacademy/objects/<model("eacademy.eacademy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eacademy.object', {
#             'object': obj
#         })

