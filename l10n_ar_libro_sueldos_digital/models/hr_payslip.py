from odoo import models, fields # type: ignore

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    art52_book_id = fields.Many2one(
        'hr.art52.book',
        string='Libro Art. 52'
    )