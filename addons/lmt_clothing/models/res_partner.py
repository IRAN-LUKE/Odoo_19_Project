from odoo import api, fields, models


class ResPartnerInherit(models.Model):

    _inherit = 'res.partner'

    # changed the model user for employee
    employee_job_id = fields.Many2one('hr.job', string="Job Position", related='user_ids.employee_job_id')

