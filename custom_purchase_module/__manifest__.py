# -*- coding: utf-8 -*-
{
    # 'name': "custom_purchase_module",
    'name': 'Custom Purchase Module',

    'sequence': 2,
    'author': 'Anil kushwaha',

    'summary': 'A replication of the Purchase module',

    'description': """ Long description of module's purpose """,


    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    'category': 'Purchases',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',

        'views/purchase_order_views.xml',
        'wizard/purchase_transactions_report_wizard.xml',
        'wizard/purchase_transaction_PDF_report.xml',
    ],
    'installable': True,
    'application': True,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

