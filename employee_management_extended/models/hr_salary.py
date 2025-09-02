from odoo import models, fields

class HrSalary(models.Model):
    _name = 'hr.salary'
    _description = 'Salary'

    category_id = fields.Many2one('hr.categorias', string="Category", required=True, help="Categoría asociada")
    category_cct_id = fields.Many2one('hr.cct', string="CCT", related='category_id.cct_id', store=True, readonly=True, help="Convenio Colectivo de Trabajo asociado")
    basic_salary = fields.Float(string="Basic Salary", required=True, help="Sueldo básico")
    date_from = fields.Date(string="Date From", required=True, help="Fecha desde")
    date_to = fields.Date(string="Date To", required=True, help="Fecha hasta")
    homologation_date = fields.Date(string="Homologation Date", help="Fecha de homologación")
    active = fields.Boolean(string="Active", default=True, help="Indica si el registro está activo")
