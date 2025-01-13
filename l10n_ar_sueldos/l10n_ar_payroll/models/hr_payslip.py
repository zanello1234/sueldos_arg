# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrPayslipAr(models.Model):
    _inherit = 'hr.payslip'
    
    payment_method = fields.Selection(
        related='payslip_run_id.payment_method',
        string='Medio de Pago',
        store=True
    )
    
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
    
    @api.constrains('payment_method', 'bank_account_id')
    def _check_bank_account(self):
        for record in self:
            if record.payment_method == 'transfer' and not record.bank_account_id:
                raise ValidationError(_('El empleado debe tener configurada una cuenta bancaria para el pago por transferencia'))
