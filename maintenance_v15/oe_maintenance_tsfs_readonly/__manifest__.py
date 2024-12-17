# -*- coding: utf-8 -*-
{
    'name': 'Maintenance, Timesheet, Field Service Readonly',
    'version': '1.0.0.0',
    'summary': 'Maintenance, Timesheet, Field Service Readonly',
    'description': 'Maintenance, Timesheet, Field Service Readonly',
    'category': 'Maintenance',
    'author': 'Mohamed Sherif',
    # 'website': '',
    # 'license': '',
    'depends': ['base', 'maintenance', 'industry_fsm', 'project','ae_maintenance_contract'],
    'data': [
        'security/security.xml',
        'views/res_company.xml',
    ],
    'installable': True,
    'auto_install': False,
}
