# -*- coding: utf-8 -*-
# from odoo import http


# class PdfReportInherit(http.Controller):
#     @http.route('/pdf_report_inherit/pdf_report_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pdf_report_inherit/pdf_report_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pdf_report_inherit.listing', {
#             'root': '/pdf_report_inherit/pdf_report_inherit',
#             'objects': http.request.env['pdf_report_inherit.pdf_report_inherit'].search([]),
#         })

#     @http.route('/pdf_report_inherit/pdf_report_inherit/objects/<model("pdf_report_inherit.pdf_report_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pdf_report_inherit.object', {
#             'object': obj
#         })

