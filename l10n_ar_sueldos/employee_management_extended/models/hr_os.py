from odoo import models, fields, api

class HrOs(models.Model):
    _name = 'hr.os'
    _description = 'Obra Social'

    name = fields.Char(string="Obra social", required=True, help="Nombre dela Os.")
    code = fields.Char(string="Código de la obra social", required=True, help="Código de la Os.")
