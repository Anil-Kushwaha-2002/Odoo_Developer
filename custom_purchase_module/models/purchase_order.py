from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _name = 'custom.purchase.order'
    _description = 'Custom Purchase Order'

    _order = 'name asc'

    # Basic Fields
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, change_default=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id.id)
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    date_arrival = fields.Date(string='Expected Arrival',)

    # One2many Field for Invoice Lines
    order_line_ids = fields.One2many('custom.purchase.order.line', 'order_id', string="Order Line")
    order_line = fields.One2many('custom.purchase.order.line', 'order_id', string='Order Lines' )

    # Computed Fields
    amount_untaxed = fields.Float(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',track_visibility='onchange')
    amount_tax = fields.Float(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_amount_all')

    # Additional Info Fields
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    source_document = fields.Char(string='Source Document')
    payment_terms_id = fields.Many2one('account.payment.term', string='Payment Terms')
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')


    # _amount_all :-

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })


    def action_send_email(self):
        template_id = self.env.ref('your_module.email_template_id').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
        _logger.info(f"Email sent for order {self.name}")

    def action_print_rfq(self):
        # Logic to print RFQ, This would typically trigger a report print action
        _logger.info(f"Printing RFQ for order {self.name}")

    def action_confirm_order(self):
        # Logic to confirm order
        self.write({'state': 'confirmed'})
        _logger.info(f"Order {self.name} confirmed")

    def action_cancel_order(self):
        # Logic to cancel order
        self.write({'state': 'cancelled'})
        _logger.info(f"Order {self.name} cancelled")


    # Defined sequence in your model
    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            # Generate a new sequence number
            seq = self.env['ir.sequence'].next_by_code('purchase.order') or ('New')
            vals['name'] = seq
        return super(PurchaseOrder, self).create(vals)



class PurchaseOrderLine(models.Model):
    _name = 'custom.purchase.order.line'
    _description = 'Custom Purchase Order Line'

    # # Order Lines Fields
    order_id = fields.Many2one('custom.purchase.order', string='Order Reference')
    product_id = fields.Many2one('product.product', string='Product')
    name = fields.Text(string='Name Desc')
    product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')

    # Additional Info Fields
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    source_document = fields.Char(string='Source Document')
    payment_terms_id = fields.Many2one('account.payment.term', string='Payment Terms')
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')

    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', readonly=True, store=True)
    price_total = fields.Float(compute='_compute_amount', string='Total', readonly=True, store=True)


    # _compute_amount :- method which calculates the price_subtotal, price_tax, and price_total

    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        tax_rate = 0.15  # Assuming a 15% tax rate
        for line in self:
            # Calculate the subtotal as the product of quantity and unit price
            line.price_subtotal = line.product_qty * line.price_unit
            # Calculate the tax based on the subtotal
            line.price_tax = line.price_subtotal * tax_rate
            # Calculate the total price by adding the subtotal and tax
            line.price_total = line.price_subtotal + line.price_tax










# from odoo import models, fields, api
#
# class PurchaseOrder(models.Model):
#     _name = 'custom.purchase.order'
#     _description = 'Custom Purchase Order'
#
#     name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
#     partner_id = fields.Many2one('res.partner', string='Vendor', required=True, change_default=True, tracking=True)
#     date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
#     # order_line = fields.One2many('custom.purchase.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
#     # amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', tracking=4)
#     amount_total = fields.Monetary(string='Total Amount', currency_field='currency_id')
#     currency_id = fields.Many2one('res.currency', string='Currency')
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('confirmed', 'Confirmed'),
#         ('done', 'Done'),
#         ('cancelled', 'Cancelled'),
#     ], string='Status', default='draft')
#
#
#     @api.depends('order_line.price_total')
#     def _amount_all(self):
#         for order in self:
#             amount_untaxed = amount_tax = 0.0
#             for line in order.order_line:
#                 amount_untaxed += line.price_subtotal
#                 amount_tax += line.price_tax
#             order.update({
#                 'amount_untaxed': order.currency_id.round(amount_untaxed),
#                 'amount_tax': order.currency_id.round(amount_tax),
#                 'amount_total': amount_untaxed + amount_tax,
#             })
