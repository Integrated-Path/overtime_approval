# -*- coding: utf-8 -*-
{
    'name': "Overtime Approvals",

    'summary': """This moulde contain Customizations that are developed by Integrated Path""",

    'description': """
       this module allow for customized overtime approval process linked with payroll

    """,

    'author': "Integrated Path",
    'website': "https://www.int-path.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '15.1',

    # any module necessary for this one to work correctly
    'depends': ['base',"approvals", "hr_payroll"],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/rules.xml',
        'views/views.xml',
        
    ],
}
