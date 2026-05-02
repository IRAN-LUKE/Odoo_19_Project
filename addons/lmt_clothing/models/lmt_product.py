from odoo import api, fields, models


class LMTProduct(models.Model):
    _name = "lmt.product"
    _description = "LMT Product"
    _inherit = ['mail.thread']

    name = fields.Char(required=True, translate=True)
    is_raw_material = fields.Boolean(string="Raw Material", default=False)
    clothing_type = fields.Many2one('lmt.product.type', required=True)
    clothing_size = fields.Many2one('lmt.product.size', required=True)

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    sale_amount = fields.Float(currency_field='currency_id', string="Sales Amount", tracking=True)
    purchase_amount = fields.Float(currency_field='currency_id', string="Purchase Amount", tracking=True)
    qty = fields.Integer(string="Quantity", tracking=True)
    product_id = fields.Many2one('product.product', required=True)

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.product_id:
                rec.product_id.write({
                    'lst_price': rec.sale_amount,
                    'standard_price': rec.purchase_amount,
                })
        return res

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if rec.product_id:
            rec.product_id.write({
                'lst_price': rec.sale_amount,
                'standard_price': rec.purchase_amount,
            })
        return rec

