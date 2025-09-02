{
    'name': 'Argentina - Payroll',
    'version': '17.0.1.0.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Manage payroll for Argentina',
    'description': """
        Localización Argentina para el módulo de nómina:
        - Reglas salariales para Argentina
        - Estructuras salariales
        - Libro de Sueldos Art. 52
        - Libro de Sueldos Digital AFIP
        - Recibos de sueldo según normativa
    """,
    'author': 'OpenERP Argentina',
    'website': 'www.odoo.com',
    'depends': [
        'hr_payroll',
        'hr_contract',
        'hr',
        'l10n_ar',
    ],
    'data': [
        'views/hr_payslip_run_views.xml',
        'views/hr_payslip_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OEEL-1',
}
