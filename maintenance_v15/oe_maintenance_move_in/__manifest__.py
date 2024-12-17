# -*- coding: utf-8 -*-
{
    'name': 'Maintenance dynamic Move In',
    'version': '1.0.0.0',
    'summary': 'Maintenance dynamic Move In',
    'description': 'Maintenance dynamic move in report,by rendering html page with dynamic fields',
    'category': 'Website',
    'author': 'OdooERP.ae',
    'website': 'https://odooerp.ae',
    'depends': ['base', 'web','project'],
    'data': [

        'views/project_task_inherit.xml',
        'report/move_in_report.xml',

    ],
    'installable': True,
    'auto_install': False,
}
