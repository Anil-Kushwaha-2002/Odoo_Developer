# -*- coding: utf-8 -*-
{
    'name': ' Maintenance Access Right ',
    'sequence': 1,
    'author': 'Anil kushwaha',

    'summary': "Maintenance Access Right",
    'description': "Maintenance Access Right",
    'category': 'base, Maintenance',
    'version': '1.0',

    'depends': [
        'base','maintenance',
        'project',
    ],
    'data': [

        'security/security.xml',
        'views/menu_request_type.xml',

    ],

    'auto_install': False,
    'installable': True,

}
