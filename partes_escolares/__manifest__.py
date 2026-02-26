# -*- coding: utf-8 -*-
{
    'name': "PartesEscolares",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.1',
    'license': 'LGPL-3',

    'icon': 'static/description/icon.png',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/xml_import_wizard_view.xml',
        'reports/report_templates.xml',
        'reports/report_alumno_partes.xml',
        'reports/report_partes_activos.xml',
        'reports/report_partes_cerrados.xml',
        'views/templates.xml',
        'views/views_alumno.xml',
        'views/views_parte.xml',
        'views/views_grupo.xml',
        'views/views_profesor.xml',
        'views/views_motivo.xml',
        'views/views_aula.xml',
        'views/views.xml',
        'views/views_asignatura.xml',
        'data/data_initial.xml',
        'data/aulas.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'partes_escolares/static/src/js/alumno_list_view.js',
            'partes_escolares/static/src/xml/alumno_list_view.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}