# -*- coding: utf-8 -*-
{
    'name': "  Custom Employee  ",

    'sequence': 3,
    'author': 'Anil kushwaha',

    'category': 'Human Resources',

    'description': """ Manage employees with multi-level approval.""",


    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/employee_security.xml',

        'report/sale_report_inherit_template.xml',

         'data/employee_security_groups.xml',

        'views/views.xml',
        'views/templates.xml',

        'views/employee_views.xml',

    ],

    'installable': True,
    'application': True,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

