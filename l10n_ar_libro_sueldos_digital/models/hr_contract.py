from odoo import models, fields # type: ignore

class HrContract(models.Model):
    _inherit = 'hr.contract'

    art52_book_id = fields.Many2one('hr.art52.book', string='Libro Art. 52')