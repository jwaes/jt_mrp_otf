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
    'depends': ['mrp','mrp_subcontracting','stock','project'],

    # always loaded
    'data': [
        'report/sale_report_templates.xml',
        'security/ir.model.access.csv',
        'views/mrp_bom_views.xml',
        'views/otf_bom.xml',
        'views/product_views.xml',
        'views/project_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
