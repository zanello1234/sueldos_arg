from odoo import models, fields, api
from datetime import datetime

class EmployeeSanction(models.Model):
    _name = 'hr.employee.sanction'
    _description = 'Registro de Sanciones de Empleados'
    _order = 'date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Referencia', 
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo'
    )
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True,
        tracking=True
    )
    
    date = fields.Date(
        string='Fecha de Sanción',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    
    reason = fields.Text(
        string='Motivo',
        required=True,
        tracking=True
    )
    
    company_id = fields.Many2one(
    'res.company',
    string='Empresa',
    default=lambda self: self.env.company,
    required=True
)

    
    sanction_type = fields.Selection([
        ('warning', 'Advertencia'),
        ('written_warning', 'Amonestación Escrita'),
        ('suspension', 'Suspensión'),
        ('termination', 'Despido')
    ], string='Tipo de Sanción', required=True, tracking=True)
    
    description = fields.Html(
        string='Descripción del Caso',
        help="Descripción detallada de los hechos y la sanción aplicada"
    )
    
    suspension_days = fields.Integer(
        string='Días de Suspensión',
        help="Aplicable solo para sanciones tipo 'Suspensión'",
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', tracking=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
                if vals.get('name', 'Nuevo') == 'Nuevo':
                    vals['name'] = self.env['ir.sequence'].with_context(
                force_company=self.env.user.company_id.id
            ).next_by_code('hr.employee.sanction') or 'Nuevo'
        return super().create(vals_list)

    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.onchange('sanction_type')
    def _onchange_sanction_type(self):
        if self.sanction_type != 'suspension':
            self.suspension_days = 0
