# -*- coding: utf-8 -*-
{
    'name': "inspire_approval",

    'summary': "Purchases Approvals",

    'description': """
Long description of module's purpose
    """,

    'author': "inspirehub",
    'website': "https://www.inspirehub.net/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'app',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','hr','approvals'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/notify.xml',
        'views/request.xml',
        'views/approvers.xml',
        'views/views.xml',
        'views/order_type.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

