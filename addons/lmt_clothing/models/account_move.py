from odoo import api, fields, models


class AccountMoveInherit(models.Model):

    _inherit = 'account.move'

    lmt_purchase_id = fields.Many2one(
        'lmt.purchase.order',
        string="LMT Purchase Order",
        ondelete='set null',
        index=True,
    )

    lmt_sale_id = fields.Many2one(
        'lmt.sale.order',
        string="LMT Sale Order",
        ondelete='set null',
        index=True,
    )

