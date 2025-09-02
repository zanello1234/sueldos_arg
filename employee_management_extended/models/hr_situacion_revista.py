from odoo import models, fields, api

class HrSituacionRevista(models.Model):
    _name = 'hr.situacion.revista'
    _description = 'Situación de Revista'
    
    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string="cod_sit", required=True)
   
