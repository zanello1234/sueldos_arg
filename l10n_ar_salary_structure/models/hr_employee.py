from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    payslip_count = fields.Integer(compute='_compute_payslip_count', string='Payslip Count')

    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = self.env['hr.payslip'].search_count([('employee_id', '=', employee.id)])

    def action_view_payslip(self):
        self.ensure_one()
        return {
            'name': 'Employee Payslips',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }