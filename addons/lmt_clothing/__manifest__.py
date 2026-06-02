# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and  licensing details.

{
    'name': 'LMT Clothing Store',
    'category': 'custom',
    'version': '1.0',
    'depends': ['base', 'product', 'mail', 'account', 'sale', 'stock', 'purchase', 'hr'],
    'author': 'Lwin Minn Thant',
    'license': 'LGPL-3',
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence.xml",
        "views/lmt_product_views.xml",
        "views/lmt_product_category_views.xml",
        "views/lmt_product_size_views.xml",
        "views/hr_employee_views.xml",
        "views/res_partner_views.xml",
        "views/res_users_views.xml",
        "views/lmt_sale_order_views.xml",
        "views/lmt_purchase_order_views.xml",
        "views/account_move_bill_views.xml",
        "views/account_move_invoice_views.xml",
        "views/hr_job_views.xml",
        "views/menus.xml",
    ],

    'auto_install': False,
}
