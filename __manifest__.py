# -*- coding: utf-8 -*-
{
    'name': 'Scraping de Ofertas de trabajo',
    'version': '1.0',
    'summary': """ Módulo que trae ofertas desde portales de trabajos """,
    'author': 'Breithner Aquituari',
    'website': '',
    'category': '',
    'depends': ['base', ],
    "data": [
        "security/ir.model.access.csv",
        "views/menu_views.xml",
        "views/job_portal_source_views.xml",
        "views/job_portal_views.xml",
        "wizards/job_portal_search_wizard.xml"
    ],
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
