# -*- coding: utf-8 -*-
{
    'name': 'Argentina - Payslip',
    'version': '17.0.1.0.0',
    'category': 'Human Resources/Payroll',
    'summary': 'Manage payslip for Argentina',
    'depends': [
        'hr_payroll',
        'hr_contract',
        'employee_management_extended',
        'l10n_ar',
        'l10n_ar_payroll',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/paper_format.xml',
        'report/payslip_report.xml',        # Primero cargamos el reporte
        'views/hr_payslip_views.xml',       # Luego las vistas que lo referencian
        'views/sign_views.xml',            # Luego las vistas para la firma
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
