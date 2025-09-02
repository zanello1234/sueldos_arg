from odoo import models, fields

class HrConceptosAfip(models.Model):
    _name = 'hr.conceptos.afip'
    _description = 'Conceptos AFIP'
    _rec_name = 'codigo'

    codigo = fields.Char(string='Código', required=False)
    descripcion = fields.Text(string='Descripción', required=False)