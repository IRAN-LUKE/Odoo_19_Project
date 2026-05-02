from odoo import api, fields, models


class ResPartnerInherit(models.Model):

    _inherit = 'res.partner'

    employee_role = fields.Selection(
        [
            ('sale', 'Salesperson'),
            ('purchase', 'Purchasing / Dealer'),
            ('manager', 'Assistant Manager'),
            ('mrp', 'Manufacturing Officer'),
        ],
        related='user_ids.employee_role',
        store=True,
        readonly=True
    )

