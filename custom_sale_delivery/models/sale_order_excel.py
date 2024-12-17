from io import BytesIO
import base64
import xlsxwriter
from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_download_excel(self):
        # Get the active_ids (selected records)
        active_ids = self.env.context.get('active_ids', [])

        if not active_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                'message': 'No records selected!',
            }

        # Create an in-memory output file for the Excel file
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Add headers to the Excel file

        worksheet.write(0, 0, 'Order Number')
        worksheet.write(0, 1, 'Customer')
        worksheet.write(0, 2, 'Order Date')
        worksheet.write(0, 3, 'Salesperson')
        worksheet.write(0, 4, 'Status')
        worksheet.write(0, 5, 'Expected Date')
        worksheet.write(0, 6, 'Total')

        # Add data from selected sale orders
        row = 1
        for order in self.browse(active_ids):
            worksheet.write(row, 0, order.name)
            worksheet.write(row, 1, order.partner_id.name)
            worksheet.write(row, 2, str(order.date_order))
            worksheet.write(row, 3, order.user_id.name if order.user_id else 'N/A')
            worksheet.write(row, 4, order.state)
            worksheet.write(row, 5, str(order.expected_date) if hasattr(order, 'expected_date') and order.expected_date else 'N/A')
            worksheet.write(row, 6, order.amount_total)
            row += 1

        # Close the workbook and get the file content
        workbook.close()
        file_data = base64.b64encode(output.getvalue())
        output.close()

        # Create an attachment for the Excel file
        attachment = self.env['ir.attachment'].create({
            'name': 'Sales_Orders.xlsx',
            'type': 'binary',
            'datas': file_data,
            'store_fname': 'Sales_Orders.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        # Return the attachment as a download URL
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

