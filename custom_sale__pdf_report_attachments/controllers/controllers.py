# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSalePdfReportAttachments(http.Controller):
#     @http.route('/custom_sale__pdf_report_attachments/custom_sale__pdf_report_attachments', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sale__pdf_report_attachments/custom_sale__pdf_report_attachments/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sale__pdf_report_attachments.listing', {
#             'root': '/custom_sale__pdf_report_attachments/custom_sale__pdf_report_attachments',
#             'objects': http.request.env['custom_sale__pdf_report_attachments.custom_sale__pdf_report_attachments'].search([]),
#         })

#     @http.route('/custom_sale__pdf_report_attachments/custom_sale__pdf_report_attachments/objects/<model("custom_sale__pdf_report_attachments.custom_sale__pdf_report_attachments"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sale__pdf_report_attachments.object', {
#             'object': obj
#         })

