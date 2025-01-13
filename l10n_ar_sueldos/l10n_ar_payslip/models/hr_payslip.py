# l10n_ar_payslip/models/hr_payslip.py
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from num2words import num2words

class HrPayslipAr(models.Model):
    _inherit = 'hr.payslip'
    
    payment_type = fields.Selection([
        ('transfer', 'Transferencia Bancaria'),
        ('check', 'Cheque'),
        ('cash', 'Efectivo')
    ], string='Medio de Pago', required=True, default='transfer')
    
    bank_account_id = fields.Many2one(
        'res.partner.bank',
        string='Cuenta Bancaria',
        domain="[('partner_id', '=', employee_id)]"
    )
    
    payment_date = fields.Date(
        string='Fecha de Pago',
        required=True,
        default=fields.Date.context_today
    )
    
    number = fields.Char(
        string='Número de Recibo',
        readonly=True,
        copy=False
    )
    
    net_salary_in_words = fields.Char(
        string='Salario Neto en Texto', 
        compute='_compute_net_salary_in_words'
    )
    
    # Agregar el campo amount_total
    amount_total = fields.Float(
        string='Importe Total'
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('number'):
                vals['number'] = self.env['ir.sequence'].next_by_code('hr.payslip.ar')
        return super().create(vals_list)
    
    @api.onchange('payment_type')
    def _onchange_payment_type(self):
        if self.payment_type != 'transfer':
            self.bank_account_id = False
    
    def action_payslip_done(self):
        for slip in self:
            if slip.payment_type == 'transfer' and not slip.bank_account_id:
                raise ValidationError(_('Debe especificar una cuenta bancaria para pagos por transferencia.'))
        return super().action_payslip_done()
    
    def _compute_net_salary_in_words(self):
        for slip in self:
            salario_basico = 0
            remunerativos = 0
            deducciones = 0
            
            for line in slip.line_ids:
                if line.category_id.code == 'BASIC':
                    salario_basico += line.total
                elif line.category_id.code == 'ALW':
                    remunerativos += line.total
                elif line.category_id.code == 'DED':
                    deducciones += line.total
                    
            salario_neto = salario_basico + remunerativos + deducciones
            slip.net_salary_in_words = num2words(salario_neto, lang='es') + ' pesos'
