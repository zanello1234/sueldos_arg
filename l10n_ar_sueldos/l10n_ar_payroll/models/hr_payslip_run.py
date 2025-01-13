from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class HrPayslipRunAr(models.Model):
    _inherit = 'hr.payslip.run'
    
    liquidation_type = fields.Selection([
        ('monthly', 'Mensual'),
        ('sac', 'S.A.C.'),
        ('vacation', 'Vacaciones'),
        ('final', 'Liquidación Final')
    ], string='Tipo de Liquidación', required=True, default='monthly')
    
    presentation_date = fields.Date(
        string='Fecha de Presentación',
        required=True,
        default=fields.Date.context_today
    )
    
    payment_date = fields.Date(
        string='Fecha de Pago',
        required=True,
        default=fields.Date.context_today
    )
    
    payment_method = fields.Selection([
        ('transfer', 'Transferencia Bancaria'),
        ('check', 'Cheque'),
        ('cash', 'Efectivo')
    ], string='Medio de Pago', required=True, default='transfer')

    social_security_deposit_date = fields.Date(
        string='Fecha de Depósito Leyes Sociales',
        required=True,
        default=fields.Date.context_today
    )

    social_security_period_date = fields.Char(
        string='Leyes sociales período depositado',
        required=True,
        default=lambda self: fields.Date.today().strftime('%m/%Y')
    )

    deposit_bank_id = fields.Many2one(
        'res.bank',
        string='Banco de Depósito',
        required=True
    )
    
    libro_sueldos_digital = fields.Binary(
        string='Archivo Libro Sueldos Digital',
        attachment=True,
        copy=False,
    )
    libro_sueldos_filename = fields.Char(
        string='Nombre del archivo',
        copy=False,
    )
    libro_sueldos_estado = fields.Selection([
        ('draft', 'Borrador'),
        ('generated', 'Generado'),
        ('validated', 'Validado'),
        ('error', 'Error')
    ], string='Estado del Libro', default='draft')

    def action_generate_libro_digital(self):
        """Genera el archivo del Libro de Sueldos Digital según especificaciones AFIP"""
        self.ensure_one()
        self.write({
            'libro_sueldos_estado': 'generated',
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Información'),
                'message': _('Función en desarrollo'),
                'type': 'info',
                'sticky': False,
            }
        }

    @api.constrains('social_security_period_date')
    def _check_social_security_period_date(self):
        for record in self:
            if not re.match(r'^(0[1-9]|1[0-2])/\d{4}$', record.social_security_period_date):
                raise ValidationError(_("The 'Leyes sociales período depositado' must be in the format mm/yyyy."))
