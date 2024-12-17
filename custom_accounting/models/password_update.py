from odoo import models, api
from odoo.exceptions import AccessError

class ResUsers(models.Model):
    _inherit = 'res.users'

    # @api.model
    # def update_all_users_password(self, new_password):
    #     """Update the password for all users in the system."""
    #     # Ensure only system administrators can execute this function
    #     if not self.env.user.has_group('base.group_system'):
    #         raise AccessError("You do not have the necessary permissions to perform this action.")
    #
    #     users = self.search([])
    #     for user in users:
    #         user.password = '123'  # This will hash the password automatically
    #     return True




