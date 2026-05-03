from odoo import api, fields, models


class LMTProductCategory(models.Model):
    _name = "lmt.product.category"
    _description = "LMT Product Category"

    name = fields.Char(required=True)
