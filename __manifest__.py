{
    'name': 'OpenAcademy',
    'version': '1.0',
    'author': 'Odoo S.A',
    'website': 'odoo.com',

    'depends': ['base'],
    'data': ['controllers/openacademy_template.xml',
            'report/openacademy_session_report.xml',
            'wizard/openacademy_wizard_view.xml',
            'views/openacademy_views.xml',
             'views/res_partner_view_inherit.xml',
             'security/openacademy_security.xml',
             'security/ir.model.access.csv'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3'

}