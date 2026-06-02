{
    'name': 'Low Stock Replenishment System',
    'category': 'custom',
    'summary': 'Shows products below minimal qty and lets you create a Purchase Order',
    'version': '1.1',
    'depends': ['lmt_clothing'],
    'author': 'Lwin Minn Thant',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/minimal_stock_qty_views.xml',
        'views/low_stock_product_views.xml',
        'views/menus.xml',
    ],
    'auto_install': False,
}
