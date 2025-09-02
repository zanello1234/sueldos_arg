from odoo import models, fields

class HrCCT(models.Model):
    _name = 'hr.cct'
    _description = 'Convenios colectivos'

    code = fields.Char(string="Code", required=True, help="Código CCT")
    name = fields.Char(string="Name", required=True, help="Nombre de la CCT.")
    categoria_ids = fields.One2many('hr.categorias', 'cct_id', string="Categorías", help="Categorías asociadas al CCT")
    activar = fields.Boolean(string="Activar", help="Campo para activar o desactivar el registro", store=True)
    union_id = fields.Many2one('hr.union', string="Union", help="Sindicato asociado")
