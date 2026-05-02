from odoo import api, fields, models


class LMTSaleOrder(models.Model):
    _name = "lmt.sale.order"
    _description = "LMT Sale Order"
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    datetime = fields.Datetime(default=fields.Datetime.now)
    customer_id = fields.Many2one('res.partner', string="Customer")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation'),
        ('sale', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ])
    so_line_ids = fields.One2many('lmt.sale.order.line', 'order_id')

class LMSaleOrderLine(models.Model):
    _name = 'lmt.sale.order.line'
    _description = "LMT Sale Order Line"
    _inherit = ['mail.thread']

    order_id = fields.Many2one('lmt.sale.order')
    product_id = fields.Many2one('product.product')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    qty = fields.Integer(string="Quantity")
    price_unit = fields.Float(string="Unit Price")
    discount_amount = fields.Float(string="Disc Amount")
    total_amount = fields.Monetary(string="Total Amount", currency_field='currency_id', compute='_compute_total_amount')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                lmt_product = self.env['lmt.product'].search(
                    [('product_id', '=', line.product_id.id)],
                    limit=1
                )
                line.price_unit = lmt_product.sale_amount or 0.0

    @api.depends('qty', 'price_unit', 'discount_amount')
    def _compute_total_amount(self):
        for line in self:
            line.total_amount = (line.price_unit * line.qty) - line.discount_amount

