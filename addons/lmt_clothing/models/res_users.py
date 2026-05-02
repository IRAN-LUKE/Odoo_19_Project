from odoo import api, fields, models


class ResUsersInherit(models.Model):

    _inherit = 'res.users'

    employee_role = fields.Selection([
        ('sale', 'Salesperson'),
        ('purchase', 'Purchasing / Dealer'),
        ('manager', 'Assistant Manager'),
        ('mrp', 'Manufacturing Officer'),
    ], string="Role")