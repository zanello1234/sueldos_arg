from odoo import models, fields, api # type: ignore
from datetime import datetime
import base64

class HrArt52Book(models.Model):
    _name = 'hr.art52.book'
    _description = 'Libro Especial Art. 52 LCT'

    name = fields.Char(string='Name', required=True)
    date = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.context_today,
    )
    number = fields.Char('Número')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('printed', 'Printed')
    ], string='Status', default='draft')
    fecha_presentacion = fields.Date(string='Fecha de Presentación', readonly=True)
    tipo_empresa = fields.Selection([
        ('0', 'Administración Pública'),
        ('1', 'Decreto 814/01, Art2 Inc.B'),
        ('2', 'Servicios Eventuales, Art2 Inc.B'),
        ('4', 'Decreto 814/01, Art2 Inc.A'),
        ('5', 'Servicios Eventuales, Art2 Inc.A'),
        ('7', 'Enseñanza Privada'),
        ('8', 'Decreto 1212/03 - AFA Clubes')
    ], string="Tipo de Empresa", help="Tipo de empresa según la clasificación.")
    identificacion_envio = fields.Selection([
        ('SJ', 'SJ - Liquidación de SyJ y DJ F931'),
        ('RE', 'RE - Solo DJ F931')
    ], string='Identificación de Envío', required=True)
    tipo_liquidacion = fields.Selection([
        ('M', 'Mensual'),
        ('Q', 'Quincenal'),
        ('D', 'Diario'),
        ('H', 'Por Hora')
    ], string='Tipo de Liquidación', required=True)
    numero_liquidacion = fields.Integer(string='Número de Liquidación', required=True)
    txt_file = fields.Binary(string='Archivo TXT', attachment=True)
    txt_filename = fields.Char(string='Nombre archivo')
    acuse_recibo = fields.Binary(string='Acuse de recibo', attachment=True)
    acuse_recibo_filename = fields.Char(string='Nombre Acuse')
    payslip_run_id = fields.Many2one('hr.payslip.run', 
        string='Lote de Recibos',
        required=True,
        help='Lote de recibos de sueldo del período')
    
    employee_ids = fields.Many2many(
        'hr.employee',
        string='Empleados',
        compute='_compute_employee_ids',
        store=True
    )
    
    payslip_ids = fields.Many2many(
        'hr.payslip',
        string='Recibos de Sueldo',
        compute='_compute_payslip_ids',
        store=True
    )
    
    payslip_payment_type = fields.Selection(
        related='payslip_ids.payment_type',
        string='Medio de Pago',
        store=True
    )

    payslip_state = fields.Selection(
        related='payslip_ids.state',
        string='Estado del Recibo',
        store=True
    )

    # Datos del empleado para el libro
    children = fields.Integer(related='employee_ids.children',
        string='Hijos', store=True)
    bank_account_id = fields.Many2one(related='employee_ids.bank_account_id',
        string='Cuenta Bancaria', store=True)
    situacion_revista_id = fields.Many2one(related='employee_ids.situacion_revista_id', 
        string='Situación de Revista', store=True)
    marca_cct = fields.Boolean(related='employee_ids.marca_cct', 
        string='Marca CCT', store=True)
    svo = fields.Boolean(related='employee_ids.svo', 
        string='SVO', store=True)
    obra_social = fields.Many2one(related='employee_ids.obra_social', 
        string='Obra Social', store=True)
    legajo = fields.Char(related='employee_ids.legajo', 
        string='Legajo', store=True)

    # Datos del contrato para el libro
    contract_ids = fields.One2many(
        'hr.contract', 
        'art52_book_id',  # inverse field name that will be created in hr.contract
        string='Contratos',
        compute='_compute_contract_ids',
        store=True
    )

    reg01_txt = fields.Text(
        string='Registro 01',
        compute='_compute_reg01_txt',
        store=True
    )
    
    reg02_txt = fields.Text(
        string='Registro 02', 
        compute='_compute_reg02_txt',
        store=True
    )
    
    reg03_txt = fields.Text(
        string='Registro 03',
        compute='_compute_reg03_txt', 
        store=True
    )
    
    reg04_txt = fields.Text(
        string='Registro 04',
        compute='_compute_reg04_txt',
        store=True
    )

    payslip_line_ids = fields.One2many(
        'hr.payslip.line',
        related='payslip_ids.line_ids',
        string='Líneas de Recibo',
        readonly=True
    )

    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        required=True,
        default=lambda self: self.env.company
    )

    @api.depends('payslip_run_id.slip_ids')
    def _compute_employee_ids(self):
        for record in self:
            record.employee_ids = record.payslip_run_id.slip_ids.mapped('employee_id')

    @api.depends('payslip_run_id')
    def _compute_payslip_ids(self):
        for record in self:
            record.payslip_ids = record.payslip_run_id.slip_ids

    @api.depends('employee_ids')
    def _compute_contract_ids(self):
        for record in self:
            record.contract_ids = [(6, 0, record.employee_ids.mapped('contract_id').ids)]

    @api.onchange('payslip_run_id')
    def _onchange_payslip_run(self):
        if self.payslip_run_id:
            self.date = self.payslip_run_id.date_end

    @api.depends('payslip_run_id', 'date', 'tipo_empresa')
    def _compute_reg01_txt(self):
        for record in self:
            record.reg01_txt = record._generate_record_01()

    @api.depends('employee_ids', 'date')
    def _compute_reg02_txt(self):
        for record in self:
            record.reg02_txt = record._generate_record_02()

    @api.depends('payslip_ids', 'date')
    def _compute_reg03_txt(self):
        for record in self:
            record.reg03_txt = record._generate_record_03()

    @api.depends('employee_ids', 'tipo_empresa')
    def _compute_reg04_txt(self):
        for record in self:
            record.reg04_txt = record._generate_record_04()

    @api.model
    def create(self, vals):
        if 'payslip_run_id' in vals:
            run = self.env['hr.payslip.run'].browse(vals['payslip_run_id'])
            vals['date'] = run.date_end
        return super().create(vals)

    def _generate_record_01(self):
        self.ensure_one()
        if not self.date:
            self.date = fields.Date.context_today(self)
            
        return "01{cuit:011d}SJ{periodo:06d}M{liquidacion:05d}30{cantidad_registros:06d}{tipo_empresa}".format(
            cuit=int(self.env.company.vat or '0'),
            periodo=int(self.date.strftime('%Y%m')),
            liquidacion=1,
            cantidad_registros=len(self.employee_ids),
            tipo_empresa=self.tipo_empresa or ''
        )

    def _generate_record_02(self):
        self.ensure_one()
        records = []
        for employee in self.employee_ids:
            try:
                # Asegurar que legajo tenga exactamente 10 caracteres
                legajo = (employee.legajo or '').ljust(10)[:10]
                
                # Limpiar y validar CBU
                cbu = ''.join(filter(str.isdigit, employee.bank_account_id.acc_number or '0'))
                if len(cbu) > 22:
                    cbu = cbu[:22]
                elif len(cbu) < 22:
                    cbu = cbu.zfill(22)

                record = "02{cuil:011d}{legajo:010s}{dependencia:040s}{cbu:022s}{dias_tope:03d}{fecha_pago:08d}{fecha_rubrica:08d}{forma_pago:01d}".format(
                    cuil=int(employee.ssnid or '0'),
                    legajo=legajo,
                    dependencia='CASA CENTRAL'.ljust(40),
                    cbu=cbu,
                    dias_tope=30,
                    fecha_pago=int(self.date.strftime('%Y%m%d')),
                    fecha_rubrica=int(self.date.strftime('%Y%m%d')),
                    forma_pago=1
                )
                records.append(record)
            except Exception as e:
                continue

        return "\n".join(records)

    def _generate_record_03(self):
        self.ensure_one()
        records = []
        for slip in self.payslip_run_id.slip_ids:
            for line in slip.line_ids:
                try:
                    record = "03{cuil:011d}{codigo_concepto:010s}{cantidad:05d}{unidades:01s}{importe:015d}{debito_credito:01s}{periodo_ajuste:06d}".format(
                        cuil=int(slip.employee_id.identification_id or '0'),
                        codigo_concepto=line.salary_rule_id.code or '',
                        cantidad=int(line.quantity),
                        unidades='$',
                        importe=int(line.total),
                        debito_credito='C' if line.total >= 0 else 'D',
                        periodo_ajuste=int(self.date.strftime('%Y%m'))
                    )
                    records.append(record)
                except Exception as e:
                    continue
        return "\n".join(records)

    def _generate_record_04(self):
        self.ensure_one()
        records = []
        for employee in self.employee_ids:
            try:
                record = "04{cuil:011d}{conyuge:1s}{hijos:02d}NNNNN1{tipo_empresa:1s}{tipo_operacion:1s}{codigo_situacion:02s}{codigo_condicion:02s}{codigo_actividad:03s}{codigo_modalidad:03s}{codigo_siniestrado:02s}{codigo_localidad:02s}".format(
                    cuil=int(employee.identification_id or '0'),
                    conyuge='N',
                    hijos=0,
                    tipo_empresa=self.tipo_empresa,
                    tipo_operacion='1',
                    codigo_situacion='01',
                    codigo_condicion='01',
                    codigo_actividad='001',
                    codigo_modalidad='001',
                    codigo_siniestrado='01',
                    codigo_localidad='01'
                )
                records.append(record)
            except Exception as e:
                continue
        return "\n".join(records)

    def generate_txt_file(self):
        self.ensure_one()
        output = []
        output.append(self._generate_record_01())
        output.extend(self._generate_record_02().split('\n'))
        output.extend(self._generate_record_03().split('\n'))
        output.extend(self._generate_record_04().split('\n'))
        txt_content = "\n".join(output)
        
        filename = f'LSD_{self.date.strftime("%Y%m")}.txt'
        self.write({
            'txt_file': base64.b64encode(txt_content.encode('utf-8')),
            'txt_filename': filename,
            'state': 'generated',
            'fecha_presentacion': fields.Date.today()
        })
        return True

    def set_to_printed(self):
        self.write({'state': 'printed'})

    def download_txt(self):
        """Return the TXT file."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content?model=hr.art52.book&id=%s&field=txt_file&filename=%s'  % (self.id, self.txt_filename),
            'target': 'self',
        }