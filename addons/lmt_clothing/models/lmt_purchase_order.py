# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LMTPurchaseOrder(models.Model):
    _name = "lmt.purchase.order"
    _description = "LMT Purchase Order"
    _inherit = ['mail.thread']

    name = fields.Char(
        string="Order Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    datetime = fields.Datetime(string="Order Date", default=fields.Datetime.now)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Vendor",
        required=True, change_default=True, index=True,
        tracking=True,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('purchase', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)

    po_line_ids = fields.One2many('lmt.purchase.order.line', 'order_id', string="Order Lines")

    invoice_ids = fields.One2many('account.move', 'lmt_purchase_id', string="Bills")
    invoice_count = fields.Integer(compute='_compute_invoice_count', string="Bills")

    amount_total = fields.Monetary(
        string="Total",
        currency_field='currency_id',
        compute='_compute_amount_total',
        store=True,
    )

    @api.depends('po_line_ids.total_amount')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(
                order.po_line_ids.mapped('total_amount')
            )

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('lmt.purchase.order') or _('New')
        return super().create(vals_list)

    def action_send(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_("Only draft orders can be sent."))
        self.state = 'sent'

    def action_purchase(self):
        self.ensure_one()
        if self.state not in ('draft', 'sent'):
            raise UserError(_("Only draft or sent orders can be confirmed."))
        if not self.po_line_ids:
            raise UserError(_("You cannot confirm an order with no order lines."))

        for line in self.po_line_ids:
            if line.lmt_product_id and line.qty > 0:
                line.lmt_product_id.write({
                    'qty': line.lmt_product_id.qty + line.qty
                })

        self.state = 'purchase'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'purchase':
            for line in self.po_line_ids:
                if line.lmt_product_id and line.qty > 0:
                    line.lmt_product_id.write({
                        'qty': line.lmt_product_id.qty - line.qty
                    })
        self.state = 'cancel'

    def action_draft(self):
        self.ensure_one()
        if self.state != 'cancel':
            raise UserError(_("Only cancelled orders can be reset to draft."))
        self.state = 'draft'

    def action_create_bill(self):
        self.ensure_one()
        if self.state != 'purchase':
            raise UserError(_("You can only create a bill for a confirmed purchase order."))

        invoice_line_vals = []
        for line in self.po_line_ids:
            if not line.product_id:
                continue
            invoice_line_vals.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.lmt_product_id.name if line.lmt_product_id else line.product_id.name,
                'quantity': line.qty,
                'price_unit': line.price_unit,
                'discount': (
                    (line.discount_amount / (line.price_unit * line.qty) * 100)
                    if line.price_unit and line.qty else 0.0
                )
            }))

        if not invoice_line_vals:
            raise UserError(_("No billable lines found. Make sure all lines have a product set."))

        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_line_vals,
            'lmt_purchase_id': self.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': bill.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_bills(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('lmt_purchase_id', '=', self.id)],
            'context': {'default_move_type': 'in_invoice'},
        }


class LMTPurchaseOrderLine(models.Model):
    _name = 'lmt.purchase.order.line'
    _description = "LMT Purchase Order Line"

    order_id = fields.Many2one('lmt.purchase.order', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product (internal)")
    lmt_product_id = fields.Many2one('lmt.product', string="Product")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    qty = fields.Integer(string="Quantity", default=1, tracking=True)
    price_unit = fields.Float(string="Unit Price", tracking=True)
    discount_amount = fields.Float(string="Disc Amount")
    total_amount = fields.Monetary(
        string="Total Amount",
        currency_field='currency_id',
        compute='_compute_total_amount',
        store=True,
    )

    @api.onchange('lmt_product_id')
    def _onchange_lmt_product_id(self):
        for line in self:
            if line.lmt_product_id:
                line.product_id = line.lmt_product_id.product_id
                line.price_unit = line.lmt_product_id.purchase_amount or 0.0
                if not line.qty:
                    line.qty = 1

    @api.depends('qty', 'price_unit', 'discount_amount')
    def _compute_total_amount(self):
        for line in self:
            line.total_amount = (line.price_unit * line.qty) - line.discount_amount