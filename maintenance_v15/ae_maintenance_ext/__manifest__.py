# -*- coding: utf-8 -*-
{
    'name': 'Maintenance Extension',
    'summary': "Maintenance Extension",
    'description': "Maintenance Extension Fields many2one Changed to manytomany",
    'category': 'base,',
    'version': '1.0.0.1.0',
    'depends': [
        'base','property_management','project_building_floor_flat','ae_maintenance_contract','maintenance',
        'project',
    ],
    'data': [

        'views/maintenance.xml',

    ],

    'auto_install': False,
    'installable': True,

}
