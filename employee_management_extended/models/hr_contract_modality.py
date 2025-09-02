from odoo import models, fields, api

class HrContractModality(models.Model):
    _name = 'hr.contract.modality'
    _description = 'Contract Modality'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Modality Name', required=True)
    
