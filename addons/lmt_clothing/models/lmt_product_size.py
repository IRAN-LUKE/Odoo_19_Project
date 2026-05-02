from odoo import api, fields, models


class LMTProductSize(models.Model):
    _name = "lmt.product.size"
    _description = "LMT Product Size"
    _rec_name = "short_name"

    name = fields.Char(required=True)
    short_name = fields.Char(required=True)
