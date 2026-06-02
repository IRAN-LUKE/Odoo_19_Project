from odoo import api, fields, models


class ResUsersInherit(models.Model):

    _inherit = 'res.users'

    employee_job_id = fields.Many2one('hr.job', string="Job Position")

    # changed the model user for employee
    def action_create_employee(self):
        res = super().action_create_employee()

        for user in self:
            if user.employee_id and user.employee_job_id:
                user.employee_id.job_id = user.employee_job_id.id

        return res