from odoo import models, fields

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    concepto_afip_id = fields.Many2one(
        'hr.conceptos.afip',
        string='Concepto AFIP',
        display_name='codigo',
    )