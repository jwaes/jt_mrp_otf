# -*- coding: utf-8 -*-
{
    'name': "jt_mrp_otf",

    'summary': "JT BOM product on the fly",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '15.0.1.0.5',

    # any module necessary for this one to work correctly
    'depends': ['mrp','mrp_subcontracting','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/otf_bom.xml',
        'views/product_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
