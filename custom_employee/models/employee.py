from odoo import models, fields, api

class Employee(models.Model):
    _name = 'custom.employee'
    _description = 'Custom Employee'

    name = fields.Char(string="Name", required=True)
    age = fields.Char(string="Age")
    salary = fields.Float(string="Salary")
    designation = fields.Char(string="Designation")
    department = fields.Char(string="Department")
    date_of_joining = fields.Date(string='Date of Joining')
    date_approved = fields.Datetime(string='Date Approved')
    manager_id = fields.Many2one('res.users', string='Manager')


    # Approval States
    state = fields.Selection([
        ('draft', 'Draft'),
        ('hr_approval', 'HR Approval'),
        ('technical_approval', 'Technical Approval'),
        ('finance_approval', 'Finance Approval'),
        ('approved', 'Approved')
    ], string='State')


    # Order Lines
    order_line_ids = fields.One2many('employee.order.line', 'employee_id', string='Order Lines')


# Action methods
    def action_approve_hr(self):
        self.write({
            'state': 'hr_approval',
            'date_approved': fields.Datetime.now()
        })
        self._create_order_line('approved_by_hr')

    def action_approve_tech(self):
        self.write({
            'state': 'technical_approval',
            'date_approved': fields.Datetime.now()
        })
        self._create_order_line('approved_by_tech_manager')

    def action_approve_finance(self):
        self.write({
            'state': 'finance_approval',
            'date_approved': fields.Datetime.now()
        })
        self._create_order_line('approved_by_fin_manager')

    def action_final_approve(self):
        self.write({
            'state': 'approved',
            'date_approved': fields.Datetime.now()
        })
        self._create_order_line('approved_by_react')

    def _create_order_line(self, approval_field):
        """ Helper method to create an order line for the given approval """
        self.env['employee.order.line'].create({
            'employee_id': self.id,
            'line_date': fields.Date.today(),
            approval_field: True,
        })







class EmployeeOrderLine(models.Model):
    _name = 'employee.order.line'
    _description = 'Employee Order Line'

    employee_id = fields.Many2one('custom.employee', string='Employee', ondelete='cascade')
    line_date = fields.Date(string='Line Date')

    approved_by_hr = fields.Boolean(string='Approved by HR')
    approved_by_tech_manager = fields.Boolean(string='Approved by Technical Manager')
    approved_by_fin_manager = fields.Boolean(string='Approved by Financial Manager')
    approved_by_react = fields.Boolean(string='Approved by React')







