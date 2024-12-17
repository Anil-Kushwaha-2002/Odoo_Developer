# -*- coding: utf-8 -*-
{
    'name': ' Maintenance Extension ',
    'sequence': 2,
    'author': 'Anil kushwaha',

    'summary': "Maintenance Extension",
    'description': "Maintenance Extension Fields many2one Changed to manytomany",
    'category': 'base, Maintenance',
    'version': '1.0',

    'depends': [
        'base','maintenance',
        'project',
    ],
    'data': [

        'views/maintenance.xml',

    ],

    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',

}
