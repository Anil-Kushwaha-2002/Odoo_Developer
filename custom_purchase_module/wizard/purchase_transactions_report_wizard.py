from odoo import models, fields, api
from odoo.exceptions import ValidationError
from io import BytesIO
import xlsxwriter
import base64
import logging
_logger = logging.getLogger(__name__)

import io

class CustomPurchaseOrderWizard(models.TransientModel):
    _name = 'custom.purchase.order.wizard'
    _description = 'Custom Purchase Order Wizard'

    name = fields.Char(string='Name', required=True)
    confirm_date = fields.Datetime(string='Confirmation Date')  # Add this field

    order_id = fields.Many2one('custom.purchase.order', string='Order Reference', required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    category_id = fields.Many2one(comodel_name="product.category", string="Product Category")



    def action_po_transactions(self):
        if not self.start_date or not self.end_date:
            raise ValidationError("Please provide both start and end dates.")

        data = self._fetch_data()
        report_file = self._generate_report(data)

        attachment_obj = self.env["ir.attachment"]
        attachment_id = attachment_obj.create({
            "name": "Purchase Transactions Report.xlsx",
            "datas": report_file,
            "type": "binary",
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        download_url = "/web/content/" + str(attachment_id.id) + "?download=true"

        return {
            'type': 'ir.actions.act_url',
            'url': str(base_url) + str(download_url),
            'target': 'self',
        }

    def _fetch_data(self):
        # Ensure start_date and end_date are set
        if not self.start_date or not self.end_date:
            raise ValidationError("Start Date and End Date are required.")

        # Construct the domain
        domain = [
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
        ]

        # Add the category filter if specified
        if self.category_id:
            domain.append(('order_line.product_id.categ_id', '=', self.category_id.id))

        # Debugging: Log the constructed domain
        _logger.info(f"Domain for fetching purchase orders: {domain}")

        # Fetch the purchase orders matching the domain criteria
        purchase_orders = self.env['purchase.order'].search(domain)

        # Debugging: Log the number of orders fetched
        _logger.info(f"Number of purchase orders fetched: {len(purchase_orders)}")

        data = []
        for order in purchase_orders:
            for line in order.order_line:
                # Debugging: Log each order and line item details
                _logger.info(f"Order: {order.name}, Product: {line.product_id.name}, Quantity: {line.product_qty}")

                data.append([
                    order.name,  # PO #
                    order.partner_ref,  # VENDOR REF #
                    order.date_order.strftime('%Y-%m-%d'),  # PO DATE
                    line.product_id.name,  # PRODUCT
                    line.product_qty,  # QUANTITY
                    line.price_unit,  # UNIT PRICE
                    line.price_subtotal,  # SUBTOTAL
                ])

        return data

    def _generate_report(self, data):
        stream = BytesIO()
        workbook = xlsxwriter.Workbook(stream)
        sheet1 = workbook.add_worksheet("PURCHASE TRANSACTIONS")

        # Define formatting
        css_format = workbook.add_format({
            "bold": True,
            "font_color": "black",
            "bg_color": "#a1d38d",
            "font_size": 18,
            "align": "center",
            "border": 5,
            "valign": "vcenter",
            "text_wrap": True
        })

        # Set column widths and rows
        sheet1.set_column(0, 0, 15)
        sheet1.set_column(1, 1, 20)
        sheet1.set_column(2, 2, 20)
        sheet1.set_column(3, 3, 30)
        sheet1.set_column(4, 4, 15)
        sheet1.set_column(5, 5, 15)
        sheet1.set_column(6, 6, 20)
        sheet1.set_row(0, 35)

        # Write headers
        headers = ["PO #", "VENDOR REF #", "PO DATE", "PRODUCT", "QUANTITY", "UNIT PRICE", "SUBTOTAL"]
        sheet1.write_row(0, 0, headers, css_format)

        # Write data
        row = 1
        for record in data:
            if len(record) >= 7:  # Ensure there are at least 7 items in the record
                sheet1.write(row, 0, record[0] if record[0] else '')  # PO #
                sheet1.write(row, 1, record[1] if record[1] else '')  # VENDOR REF #
                sheet1.write(row, 2, record[2] if record[2] else '')  # PO DATE
                sheet1.write(row, 3, record[3] if record[3] else '')  # PRODUCT
                sheet1.write(row, 4, record[4] if record[4] else '')  # QUANTITY
                sheet1.write(row, 5, record[5] if record[5] else '')  # UNIT PRICE
                sheet1.write(row, 6, record[6] if record[6] else '')  # SUBTOTAL
                row += 1

        workbook.close()
        stream.seek(0)
        return base64.b64encode(stream.read()).decode('ascii')







#     def action_confirm_order(self):
#         self.order_id.write({'state': 'confirmed', 'date_order': self.confirm_date})
#         self.order_id.action_confirm_order()
#         return {
#             'type': 'ir.actions.act_window_close'
#         }
#
#
# # to open the wizard
# def open_confirm_wizard(self):
#     return {
#         'type': 'ir.actions.act_window',
#         'name': 'Confirm Purchase Order',
#         'res_model': 'custom.purchase.order.wizard',
#         'view_mode': 'form',
#         'target': 'new',
#         'context': {
#             'default_order_id': self.id,
#         },
#     }
