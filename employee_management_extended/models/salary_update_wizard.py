from odoo import api, fields, models

class SalaryUpdateWizard(models.TransientModel):
    _name = 'salary.update.wizard'
    _description = 'Wizard de Actualización de Salario'

    categoria_id = fields.Many2one('hr.categorias', string='Categoría')
    basic_salary = fields.Float(string='Salario Básico')
    homologation_date = fields.Date(string='Fecha de Homologación')
    date_from = fields.Date(string='Vigencia Desde')
    date_to = fields.Date(string='Vigencia Hasta')

    @api.model
    def default_get(self, fields_list):
        """Override default_get to load values from contract"""
        res = super().default_get(fields_list)
        
        active_id = self.env.context.get('active_id')
        if active_id:
            contract = self.env['hr.contract'].browse(active_id)
            if contract.exists() and contract.categoria_id:
                # Usando los nombres correctos de los campos
                latest_salary = self.env['hr.salary'].search([
                    ('category_id', '=', contract.categoria_id.id),
                    ('active', '=', True)
                ], order='date_from desc, create_date desc', limit=1)
                
                if latest_salary:
                    res.update({
                        'categoria_id': contract.categoria_id.id,
                        'basic_salary': latest_salary.basic_salary,
                        'homologation_date': latest_salary.homologation_date,
                        'date_from': latest_salary.date_from,
                        'date_to': latest_salary.date_to,
                    })
        return res

    def action_confirm(self):
        """Confirm the salary update"""
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        if active_id:
            contract = self.env['hr.contract'].browse(active_id)
            if contract.exists():
                # Determinar qué campo actualizar según el tipo de salario
                if contract.wage_type == 'hourly':
                    contract.write({
                        'hourly_wage': self.basic_salary
                    })
                else:
                    contract.write({
                        'wage': self.basic_salary
                    })
        return {'type': 'ir.actions.act_window_close'}
