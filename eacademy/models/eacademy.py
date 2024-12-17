from odoo import fields, models, api

class Course(models.Model):
    _name = "eacademy.course"
    _description = "Eacademy Course"

    name_seq = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default=lambda self: ('New'))
    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    course = fields.Char(string='Course')
    description = fields.Text(string='Description')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    # line_ids = fields.One2many('eacademy.course.line', 'course_id', string='Lines')
    # course_id = fields.Many2one('sale.order', string='Sale Order', required=True, ondelete='cascade')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], string='Status', default='draft', tracking=True)


    # create method defined a unique sequence (new record is created )
    @api.model
    def create(self, vals):
        if vals.get('name_seq', 'New') == 'New':
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('eacademy.course') or 'New'
        result = super(Course, self).create(vals)
        return result


    #  standard state transition methods in an Odoo model
    #  These methods can be called from buttons in the form view
    def action_start(self):
        """Set the state to 'ongoing'."""
        self.write({'state': 'ongoing'})

    def action_complete(self):
        """Set the state to 'completed'."""
        self.write({'state': 'completed'})

    def action_draft(self):
        """Reset the state to 'draft'."""
        self.write({'state': 'draft'})





class ClassSession(models.Model):
    _name = 'eacademy.classsession'
    _description = 'Eacademy Class Sessions'

    name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    duration = fields.Float(string="Duration", digits=(6, 2), help="Duration in days")

    currency_id = fields.Many2one('res.currency', string='Currency')
    day_rate = fields.Monetary(string="Day Rate")
    days = fields.Integer(string="Days")
    total_rent = fields.Monetary(string='Total Rent', compute='_compute_total_rent')

    value = fields.Float(string='Value')
    value2 = fields.Float(string='Value in Percentage', compute='_value_pc', store=True)

    # Method used to calculate a value dynamically based on other fields in the model.
    @api.depends('day_rate', 'days')
    def _compute_total_rent(self):
        for record in self:
            record.total_rent = record.day_rate * record.days

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100





# class CourseLine(models.Model):
#     _name = 'eacademy.course.line'
#     _description = 'Eacademy Course Line'
#
#     name = fields.Char(string='Name', required=True)
#     quantity = fields.Integer(string='Quantity')
#     course_id = fields.Many2one('eacademy.course', string='Course', ondelete='cascade')
#     product_id = fields.Many2one('product.product', string='Product', required=True)
#     product_qty = fields.Float(string='Quantity', required=True, default=1.0)
#     price_unit = fields.Float(string='Unit Price', required=True)
#     price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)
#     # order_id = fields.Many2one('eacademy.order', string='Order', ondelete='cascade')
#
#     @api.depends('product_qty', 'price_unit')
#     def _compute_price_subtotal(self):
#         for line in self:
#             line.price_subtotal = line.product_qty * line.price_unit






# from odoo import fields, models, api
#
# class Course(models.Model):
#     _name = "eacademy.course"
#     _description = "Eacademy Course"
#
#     name_seq = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default=lambda self: ('New'))
#     name = fields.Char(string='Name', required=True)
#     age = fields.Integer(string='Age')
#     course = fields.Char(string='Course')
#     description = fields.Text(string='Description')
#     start_date = fields.Date(string="Start Date")
#     end_date = fields.Date(string="End Date")
#
#     # name_seq = fields.Char(string="Number", required=True, copy=False, readonly=True, index=True,
#     #                        default=lambda self: self.env['ir.sequence'].next_by_code('eacademy.course') or 'New')
#     line_ids = fields.One2many('eacademy.course.line', 'course_id', string='Lines')
#     course_id = fields.Many2one('sale.order', string='Sale Order', required=True, ondelete='cascade')
#
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('ongoing', 'Ongoing'),
#         ('completed', 'Completed'),
#     ], string='Status', default='draft', tracking=True)
#
#
#     # create method: -  Override the create method to assign the sequence value when a new record is created.
#     @api.model
#     def create(self, vals):
#         if vals.get('name_seq', 'New') == 'New':
#             vals['name_seq'] = self.env['ir.sequence'].next_by_code('eacademy.course') or 'New'
#         result = super(Course, self).create(vals)
#         return result
#
#
#     def action_start(self):
#         """Set the state to 'ongoing'."""
#         self.write({'state': 'ongoing'})
#
#     def action_complete(self):
#         """Set the state to 'completed'."""
#         self.write({'state': 'completed'})
#
#     def action_draft(self):
#         """Reset the state to 'draft'."""
#         self.write({'state': 'draft'})
#
#     @api.model
#     def create(self, vals):
#         """Override create method to set the sequence number."""
#         if vals.get('name_seq', 'New') == 'New':
#             vals['name_seq'] = self.env['ir.sequence'].next_by_code('eacademy.course') or 'New'
#         return super(Course, self).create(vals)
#
#
#
# class CourseLine(models.Model):
#     _name = 'eacademy.course.line'
#     _description = 'Eacademy Course Line'
#
#     name = fields.Char(string='Name', required=True)
#     quantity = fields.Integer(string='Quantity')
#     course_id = fields.Many2one('eacademy.course', string='Course', ondelete='cascade')
#     product_id = fields.Many2one('product.product', string='Product', required=True)
#     product_qty = fields.Float(string='Quantity', required=True, default=1.0)
#     price_unit = fields.Float(string='Unit Price', required=True)
#     price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)
#     order_id = fields.Many2one('eacademy.order', string='Order', ondelete='cascade')
#
#     @api.depends('product_qty', 'price_unit')
#     def _compute_price_subtotal(self):
#         for line in self:
#             line.price_subtotal = line.product_qty * line.price_unit
#
#
#
#
# class ClassSession(models.Model):
#     _name = 'eacademy.classsession'
#     _description = 'Eacademy Class Sessions'
#
#     name = fields.Char(string="Name")
#     start_date = fields.Date(string="Start Date")
#     end_date = fields.Date(string="End Date")
#     duration = fields.Float(string="Duration", digits=(6, 2), help="Duration in days")
#
#     currency_id = fields.Many2one('res.currency', string='Currency')
#     hour_rate = fields.Monetary(string="Hour Rate")
#     hours = fields.Integer(string="Hours")
#     total_rent = fields.Monetary(string='Total Rent', compute='_compute_total_rent')
#
#
#     @api.depends('hour_rate', 'hours')
#     def _compute_total_rent(self):
#         for record in self:
#             record.total_rent = record.hour_rate * record.hours
#
