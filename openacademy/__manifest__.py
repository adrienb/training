# -*- coding: utf-8 -*-
{
    'name':        "OpenAcademy",

    'summary':
                   """
                   Openacademy
                   """,

    'description': """
        Manage course, classes, teachers, students, ...
    """,

    'author':      "Odoo",
    'website':     "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'OpenAcademy',
    'version':     '0.1',

    # any module necessary for this one to work correctly
    'depends':     ['base', 'mail'],

    'application': True,
    'installable': True,

    # always loaded
    'data':        [
        "security/openacademy_security.xml",
        "security/ir.model.access.csv",
        "data/openacademy_data.xml",
        "views/classses_views.xml",
        "views/sessions_views.xml",
        "views/partner_views.xml",
        "wizard/add_attendee_views.xml",
        "report/session_report.xml",
        "views/openacademy_menu.xml",
    ],
    # only loaded in demonstration mode
    'demo':        [],
}
