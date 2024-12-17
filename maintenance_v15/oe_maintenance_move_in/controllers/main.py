from odoo import http
from odoo.http import request


class CustomController(http.Controller):

    @http.route(['/maintenance/report/<string:identifier>'], type='http', auth="public", website=True)
    def contract_report(self, identifier, **post):
        maintenance = request.env['project.task'].search([('id', '=', identifier)], limit=1)

        values = {'doc': maintenance}


        return request.render("oe_maintenance_move_in.move_in_report", values)
