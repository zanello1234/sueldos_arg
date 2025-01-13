from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmployeeExtended(models.Model):
    _inherit = 'hr.employee'

    # Nuevos campos
    legajo = fields.Char(string="Legajo", required=True, help="Número único asignado al empleado.")
    categoria = fields.Many2one('hr.convention.category', string="Categoría", help="Categoría a la que pertenece el emplado dentro del convenio")
    fecha_ingreso = fields.Date(string="Fecha de Ingreso", help="Fecha en que el empleado empezo a trabajar en la empresa.")
    fecha_egreso = fields.Date(string="Fecha de Egreso", help="Fecha en que el empleado dejó de trabajar en la empresa.")
    fecha_accidente = fields.Date(string="Fecha de Accidente", help="Fecha en que el empleado tuvo un accidente laboral.")
    jornada_laboral = fields.Selection([
        ('completa', 'Jornada Completa'),
        ('parcial', 'Jornada Parcial')
    ], string="Jornada Laboral", required=True, default='completa', help="Tipo de jornada laboral del empleado.")
    situacion_revista_id = fields.Many2one('hr.situacion.revista', string="Situación de revista", help="")
    obra_social = fields.Many2one('hr.os', string="Obra Social", help="Obra social a la que pertenece el empleado.")
    code = fields.Char(string="Code")
    sindicado = fields.Boolean(string="Sindicado", help="Indica si el empleado está afiliado a un sindicato.")
    sindicato = fields.Many2one('hr.union', string="Sindicato", help="Sindicato al que pertenece el empleado.", domain="[('active', '=', True)]")
    cct = fields.Many2one('hr.cct', string="CCT", help="CCT al que pertenece el empleado.", domain="[('union_id', '=', sindicato)]")
    employee_leaves = fields.One2many('hr.leave', 'employee_id', string='Ausencias')
    compania_aseguradora = fields.Many2one('res.partner', string="Compañía Aseguradora", help="Compañía aseguradora del empleador.")
    status = fields.Selection([
        ('activo', 'Activo'),
        ('accidentado', 'Accidentado'),
        ('inactivo', 'Inactivo'),
    ], string="Estado", compute="_compute_status", store=True)

    #Alta temprana 
    modalidad = fields.Char(string="Modalidad de contratación", help="")
    art = fields.Many2one('res.partner', string="Nombre", help="Aseguradora de Riesgos de Trabajo del empleado.")
    accident_record_ids = fields.One2many('hr.accident.record', 'employee_id', string='Registros de Accidentes')

    # Campos para sanciones
    sanction_ids = fields.One2many(
        'hr.employee.sanction',
        'employee_id',
        string='Sanciones',
        help="Registro de sanciones aplicadas al empleado"
    )
    sanction_count = fields.Integer(
        string="Número de Sanciones",
        compute='_compute_sanction_count',
        help="Cantidad total de sanciones registradas"
    )

    # Métodos para cálculo y validación
    @api.depends('fecha_egreso', 'fecha_accidente')
    def _compute_status(self):
        for record in self:
            if record.fecha_egreso:
                record.status = 'inactivo'
            elif record.fecha_accidente:
                record.status = 'accidentado'
            else:
                record.status = 'activo'

   # Campos computados para el kanban
    dias_ausencia = fields.Integer(
        string="Días de Ausencia",
        compute='_compute_dias_ausencia',
        store=True,
        help="Total de días de ausencia"
    )
    
    dias_accidente = fields.Integer(
        string="Días por Accidente",
        compute='_compute_dias_accidente',
        store=True,
        help="Total de días por accidentes laborales"
    )
    
    sanction_count = fields.Integer(
        string="Número de Sanciones",
        compute='_compute_sanction_count',
        store=True,
        help="Cantidad total de sanciones"
    )

    cantidad_sanciones = fields.Integer(
        string="Sanciones",
        compute='_compute_sanction_count',
        store=True,
        help="Cantidad total de sanciones"
    )

    @api.depends('employee_leaves')
    def _compute_dias_ausencia(self):
        for employee in self:
            total_dias = 0
            for leave in employee.employee_leaves:
                if leave.state == 'validate':  # Solo ausencias validadas
                    total_dias += leave.number_of_days
            employee.dias_ausencia = total_dias

    @api.depends('accident_record_ids')
    def _compute_dias_accidente(self):
        for employee in self:
            total_dias = 0
            if employee.fecha_accidente:
                today = fields.Date.today()
                delta = (today - employee.fecha_accidente).days
                total_dias = max(0, delta + 1)  # +1 para incluir el día inicial
            employee.dias_accidente = total_dias

    @api.depends('sanction_ids')
    def _compute_sanction_count(self):
        for employee in self:
            count = len(employee.sanction_ids.filtered(lambda s: s.state == 'confirmed'))
            employee.sanction_count = count
            employee.cantidad_sanciones = count

    @api.onchange('sindicado')
    def _onchange_sindicado(self):
        if not self.sindicado:
            self.cct = self.env['hr.cct'].search([('name', '=', 'EXCLUIDO DE CONVENIO')], limit=1)

    @api.onchange('sindicato')
    def _onchange_sindicato(self):
        self.cct = False
