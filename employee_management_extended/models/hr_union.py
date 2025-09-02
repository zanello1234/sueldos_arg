from odoo import models, fields, api

class HrUnion(models.Model):
    _name = 'hr.union'
    _description = 'Sindicato'

    name = fields.Char(string="Sindicado", required=True, help="Nombre de sindicato.")
    code = fields.Char(string="Código de sindicato", required=True, help="Código de la sindicato.")
    active = fields.Boolean(string="Activo", default=True)
    cct_ids = fields.One2many('hr.cct', 'union_id', string="CCTs", help="Convenios colectivos asociados")
