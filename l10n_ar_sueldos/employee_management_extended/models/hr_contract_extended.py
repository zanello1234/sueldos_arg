from odoo import models, fields, api
from odoo.exceptions import UserError

class ContractExtended(models.Model):
    _inherit = 'hr.contract'

    # Campos existentes de Alta Temprana
    fecha_ingreso = fields.Date(
        string="Fecha de Ingreso",
        required=True,
        help="Fecha en que el empleado ingresó a la empresa"
    )
    modalidad = fields.Many2one(
        'hr.contract.modality',
        string="Modalidad",
        help="Modalidad de contratación"
    )
    clave = fields.Char(
        string="Clave de alta temprana",
        help="Clave de alta temprana obtenida en AFIP"
    )
    presentacion = fields.Date(
        string="Fecha presentación F855",
        help="Fecha de presentación del alta"
    )
    tipo_servicio = fields.Char(
        string="Tipo de servicio",
        help="Tipo de servicio"
    )
    art = fields.Many2one(
        'res.partner',
        string="ART",
        help="Aseguradora de Riesgos de Trabajo del empleado"
    )

    # Campo nuevo para comprobante de alta temprana
    comprobante_alta_temprana = fields.Binary(
        string="Comprobante de Alta Temprana",
        help="Adjuntar comprobante de alta temprana en formato PDF",
        attachment=True
    )
    comprobante_alta_temprana_filename = fields.Char(
        string="Nombre del archivo de comprobante de alta temprana"
    )

    # Nuevos campos para informes médicos
    fecha_preocupacional = fields.Date(
        string="Informe Preocupacional de fecha",
        help="Fecha del informe preocupacional"
    )
    informe_preocupacional = fields.Binary(
        string="Informe Preocupacional",
        help="Adjuntar informe preocupacional en formato PDF",
        attachment=True
    )
    informe_preocupacional_filename = fields.Char(
        string="Nombre del archivo preocupacional"
    )

    fecha_posocupacional = fields.Date(
        string="Informe Posocupacional de fecha",
        help="Fecha del informe posocupacional"
    )
    informe_posocupacional = fields.Binary(
        string="Informe Posocupacional",
        help="Adjuntar informe posocupacional en formato PDF",
        attachment=True
    )
    informe_posocupacional_filename = fields.Char(
        string="Nombre del archivo posocupacional"
    )

    # Nuevos campos para CCT y categoría
    employee_cct = fields.Many2one(
        related='employee_id.cct',
        string='CCT',
        readonly=True,
        help='Convenio colectivo del empleado'
    )
    categoria_id = fields.Many2one(
        'hr.categorias',
        string='Categoría',
        domain="[('cct_id', '=', employee_cct)]",
        help='Categoría filtrada por el CCT del empleado'
    )

    salary = fields.Float(string='Salary')
    confirm_update = fields.Boolean(string='Confirm Update')

    def update_salary(self):
        self.ensure_one()

        # Mostrar una ventana emergente simple
        return {
            'name': 'Update Salary',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.contract',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_salary': self.salary,
                'default_confirm_update': True,
            },
        }

    @api.onchange('confirm_update')
    def _onchange_confirm_update(self):
        if self.confirm_update:
            self.salary = self.env.context.get('default_salary', 0.0)
