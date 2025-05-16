# -*- coding: utf-8 -*-
{
    'name': "eacademy",
    'sequence': 1,
    'author': 'Anil kushwaha',

    'summary': "Eacademy is a Education purpose ",

    'description': """ Detailed overview of the courses available in the eAcademy system.
 """,

    # 'author': "My Company",
    'website': "https://www.linkedin.com/in/anil-kushwaha-518114220/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',
    'license': 'LGPL-3',


    # any module necessary for this one to work correctly
    'depends': ['base','web', 'sale','purchase', 'sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/eacademy_security.xml',

        'data/sequence_data.xml',

        # 'report/sale_order_report_templates.xml',
        # 'report/sale_order_report.xml',
        'report/eacademy_report.xml',
        'report/report_template.xml',
        'report/sale_report_template.xml',

        'views/views.xml',
        'views/templates.xml',
        'views/eacademy.xml',
        'views/intern_view.xml',

        'views/sale_order_inherit_view.xml',
        'views/sale_order_line_view.xml',
        'views/purchase_order_line.xml',
    ],

    'installable': True,
    'application': True,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

