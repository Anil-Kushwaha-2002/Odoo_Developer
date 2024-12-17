# -*- coding: utf-8 -*-
{
    'name': "custom_sale_delivery",

    'sequence': 4,
    'author': 'Anil kushwaha',

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,


    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','stock', ],


    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/views.xml',
        'views/templates.xml',

        'views/sale_order_view.xml',
        'views/sale_order_export.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

