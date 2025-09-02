from odoo import models, fields, api # type: ignore
from lxml import etree # type: ignore

class HrSalaryStructureExtended(models.Model):
    _inherit = 'hr.payroll.structure'
    
    # Many2many relation with CCT
    cct_ids = fields.Many2many(
        'hr.cct',
        string='CCT Agreements'
    )
    
    # New text field for Codigo AFIP
    codigo_afip = fields.Char(
        string='Código AFIP',
        help='Código de concepto según AFIP'
    )

    # Compute fields for smart buttons
    cct_count = fields.Integer(
        compute='_compute_cct_count',
        string='CCT Count'
    )
    payslip_count = fields.Integer(
        compute='_compute_payslip_count',
        string='Payslip Count'
    )
    
    @api.depends('cct_ids')
    def _compute_cct_count(self):
        for record in self:
            record.cct_count = len(record.cct_ids)
            
    def _compute_payslip_count(self):
        for record in self:
            record.payslip_count = self.env['hr.payslip'].search_count([
                ('struct_id', '=', record.id)
            ])

    def action_view_cct(self):
        self.ensure_one()
        return {
            'name': 'CCT Agreements',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.cct',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.cct_ids.ids)],
        }

    def action_view_payslips(self):
        self.ensure_one()
        return {
            'name': 'Payslips',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip',
            'view_mode': 'tree,form',
            'domain': [('struct_id', '=', self.id)],
        }