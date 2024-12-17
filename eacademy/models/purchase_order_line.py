from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    name = fields.Char(string='name')
    pro_no = fields.Integer(string="Pro_no")
    product_details = fields.Char(string='Product Details')
    product_price = fields.Float(string='Product Price')
    details = fields.Char(string='Details')


    # _get_invoice_lines :- Method is customize, modify the behavior of a parent method in a class. ( or extend the functionality of generating invoice lines )

    def _get_invoice_lines(self, **optional_value):
        # print('click')
        # Call the parent method
        create_bill = super()._get_invoice_lines(**optional_value)
        # Ensure create_bill is a dictionary
        create_bill.update({
            "pro_no": self.pro_no,
            "product_details": self.product_details,
            "product_price": self.product_price
        })
        return create_bill



class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    pro_no = fields.Integer(string="Pro_no")
    product_details = fields.Char(string='Product Details')
    product_price = fields.Float(string='Product Price')
