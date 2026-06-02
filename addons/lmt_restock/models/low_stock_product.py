from odoo import api, fields, models
from odoo.exceptions import UserError


class LowStockProduct(models.Model):
    _name = "low.stock.product"
    _description = "Low Stock Products"

    lmt_product_id = fields.Many2one('lmt.product', string="Product")
    qty = fields.Integer(string="Current Qty", related="lmt_product_id.qty")
    minimal_qty = fields.Integer(string="Minimal Qty")
    needed_qty = fields.Integer(string="Qty to Order")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.model
    def action_open_low_stock(self):
        old_records = self.search([])
        old_records.unlink()

        config = self.env['minimal.stock.qty'].search([('is_active', '=', True)], limit=1)
        if config:
            minimal_qty = config.qty
        else:
            minimal_qty = 0

        low_products = self.env['lmt.product'].search([('qty', '<', minimal_qty)])

        for product in low_products:
            self.create({
                'lmt_product_id': product.id,
                'minimal_qty': minimal_qty,
                'needed_qty': minimal_qty - product.qty,
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Low Stock Products',
            'res_model': 'low.stock.product',
            'view_mode': 'list',
            'target': 'current',
        }

    def action_create_purchase_order(self):
        config = self.env['minimal.stock.qty'].search([('is_active', '=', True)], limit=1)
        if config:
            minimal_qty = config.qty
        else:
            minimal_qty = 0

        po = self.env['lmt.purchase.order'].create({
            'partner_id': self.env.user.partner_id.id,
        })

        for rec in self:
            qty_to_order = minimal_qty - rec.lmt_product_id.qty
            if qty_to_order <= 0:
                continue

            self.env['lmt.purchase.order.line'].create({
                'order_id': po.id,
                'lmt_product_id': rec.lmt_product_id.id,
                'product_id': rec.lmt_product_id.product_id.id,
                'qty': qty_to_order,
                'price_unit': rec.lmt_product_id.purchase_amount,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'lmt.purchase.order',
            'res_id': po.id,
            'view_mode': 'form',
            'target': 'current',
        }
