from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MinimalStockQty(models.Model):
    _name = "minimal.stock.qty"
    _description = "Minimal Stock Qty"
    _inherit = ['mail.thread']

    name = fields.Char(string="Name")
    qty = fields.Integer(string="Quantity", tracking=True)
    is_active = fields.Boolean(default=False, tracking=True)

    @api.constrains('is_active')
    def _check_only_one_active(self):
        for rec in self:
            if rec.is_active:
                existing = self.search([
                    ('is_active', '=', True),
                    ('id', '!=', rec.id),
                ], limit=1)

                if existing:
                    raise ValidationError("Only one active Minimal Stock Qty is allowed.\n"
                                          "Close the activated one first to activate another.")

