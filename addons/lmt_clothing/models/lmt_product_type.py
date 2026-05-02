from odoo import api, fields, models


class LMTProductType(models.Model):
    _name = "lmt.product.type"
    _description = "LMT Product Type"

    name = fields.Char(required=True)
