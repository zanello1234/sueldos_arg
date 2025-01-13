from odoo import models, fields

class HrCategorias(models.Model):
    _name = 'hr.categorias'
    _description = 'Categorias'

    name = fields.Char(string="Name", required=True, help="Nombre de la categoría.")
    cct_id = fields.Many2one(
        'hr.cct', 
        string="CCT", 
        help="Convenio colectivo asociado",
        domain=lambda self: [('activar', '=', True)]  # Filtra registros activos
    )
    cct_code = fields.Char(
        string="CCT Code", 
        related='cct_id.code', 
        store=True, 
        help="Código de la CCT"
    )
    cct_activar = fields.Boolean(
        string="Activo", 
        related='cct_id.activar', 
        store=True, 
        help="Esta activado"
    )
    activar = fields.Boolean(
        string="Activar", 
        help="Campo para activar o desactivar el registro"
    )

