from odoo import fields, models, api

class Intern(models.Model):
    _name = "intern.class"
    _description = "Intern of Class"

    name = fields.Char(string='Name', required=True)
    day = fields.Integer(string='Day')
    feedback = fields.Char(string='Feedback')
    name_seq = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default=lambda self: ('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], string='Status', default='draft', tracking=True)

    def action_start(self):
        self.write({'state': 'ongoing'})

    def action_complete(self):
        self.write({'state': 'completed'})

   # create method defined a unique sequence (new record is created )
    @api.model
    def create(self, vals):
        if vals.get('name_seq', 'New') == 'New':
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('intern.class') or 'New'
        result = super(Intern, self).create(vals)
        return result

# from odoo import fields, models
#
# class Intern(models.Model):
#     _name = "intern.class"
#     _description = "Intern of Class"
#
#     name = fields.Char(string='Name', required=True)
#     day = fields.Integer(string='Day')
#     feedback = fields.Char(string='Feedback')
#
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('ongoing', 'Ongoing'),
#         ('completed', 'Completed'),
#     ], string='Status', default='draft', tracking=True)
#
#     def action_start(self):
#         self.write({'state': 'ongoing'})
#
#     def action_complete(self):
#         self.write({'state': 'completed'})
