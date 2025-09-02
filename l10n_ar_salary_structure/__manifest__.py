{
    'name': 'Salary Structure Extension',
    'version': '17.0',
    'category': 'HR',
    'depends': [
        'base',
        'hr_payroll',
        'hr_contract',
        'employee_management_extended'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_payroll_structure_type.xml',
        'data/hr_payroll_structure.xml',
        'views/hr_salary_structure_views.xml',
        'views/hr_employee_views.xml',
    ],
}
