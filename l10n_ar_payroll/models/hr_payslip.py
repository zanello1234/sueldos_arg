# -*- coding: utf-8 -*-
from odoo import models, fields, api, _ # type: ignore
from odoo.exceptions import ValidationError # type: ignore

class HrPayslipAr(models.Model):
    _inherit = 'hr.payslip'
 
    bank_account_id = fields.Many2one(
        related='employee_id.bank_account_id',
        string='Cuenta Bancaria',
        readonly=True,
        store=True
    )

    categoria_id = fields.Many2one(
        'hr.categorias', 
        string='Categoria',
        related='contract_id.categoria_id',
        readonly=True,
        help='Categoria del empleado',
        store=True
    )

    cct_id = fields.Many2one(
        'hr.cct',
        string='CCT',
        related='categoria_id.cct_id',
        readonly=True,
        help='Convenio colectivo asociado',
        store=True
    )
    
