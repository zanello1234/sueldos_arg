from odoo import models, fields, api

class HrAccidentRecord(models.Model):
    _name = 'hr.accident.record'
    _description = 'Registro de Accidentes'
    _order = 'fecha_inicio desc'

    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    fecha_inicio = fields.Date(string='Fecha de inicio del siniestro', required=True)
    hora = fields.Float(string='Hora del siniestro', required=True)
    fecha_fin = fields.Date(string='Fecha de fin del siniestro')
    detalle = fields.Text(string='Detalle', required=True)
    hubo_heridos = fields.Boolean(string='¿Hubo heridos?')
    es_inculpable = fields.Boolean(string='¿Es inculpable?')
    genera_ausencia = fields.Boolean(string='¿Genera ausencia?')
    cubre_art = fields.Boolean(string='¿Lo cubre la ART?')
    fue_denunciado = fields.Boolean(string='¿Fue denunciado?')
    denuncia = fields.Binary(string='Adjunto de denuncia')
    denuncia_filename = fields.Char(string='Nombre del archivo')
