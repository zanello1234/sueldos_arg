from odoo import models, fields, api
from odoo.exceptions import UserError
import base64

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    document = fields.Binary(string='Documento', attachment=True)
    status = fields.Selection([('pending', 'Pendiente'), ('signed', 'Firmado'), ('rejected', 'Rechazado')], string='Estado de Firma', default='pending')
    amount_total = fields.Monetary(string="Total", compute="_compute_amount_total", store=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(line.amount for line in record.line_ids)

    def action_send_for_signature(self):
        # Generar el reporte PDF correctamente desde el reporte 'ir.actions.report'
        report_action = self.env.ref('l10n_ar_payslip.report_payslip_ar')
        
        # Verificar que el reporte esté definido correctamente
        if not report_action:
            raise UserError('El reporte no está definido correctamente.')
        
        
        
        # Adjuntar el PDF generado al correo electrónico
        attachment = self.env['ir.attachment'].create({
            'name': 'Recibo de Sueldo.pdf',
            'type': 'binary',
            'res_model': 'hr.payslip',
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })
        
        mail_values = {
            'subject': 'Recibo de Sueldo - Firma Pendiente',
            'body_html': 'Por favor, firma el recibo de sueldo.',
            'email_to': self.employee_id.work_email,  # O usa otro campo si es necesario
            'attachment_ids': [(4, attachment.id)],
        }
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
