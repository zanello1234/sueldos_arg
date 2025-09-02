{
    'name': 'Libro Art. 52 LCT',
    'version': '17.0.1.0.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Generación del  Libro Especial txt Art. 52 LCT e impresion',
    'author': 'OnlyOne',
    'website': 'https://www.onlyone.odoo.com',
    'depends': ['hr_payroll','l10n_ar_payroll'],  # <-- Faltaba esta coma
    'data': [
        'security/ir.model.access.csv',
        'data/hr.conceptos.afip.csv',
        'views/hr_art52_book_views.xml',
        'views/hr_conceptos_afip.xml',
        'views/hr_salary_rule_views.xml',
        'reports/art52_book_templates.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}