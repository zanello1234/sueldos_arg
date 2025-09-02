# README.md

# Custom Payslip Report Module for Odoo 17 EE

## Overview

The Custom Payslip Report module enhances the existing payslip functionality in Odoo 17 EE by adding additional fields and modifying the payslip report output. This module is designed to meet specific payroll reporting requirements.

## Features

- Adds the following fields to the payslip:
  - **Nro de Seguridad Social (ssnid)**
  - **Fecha de Egreso (fecha_egreso)**
  - **Fecha de Pago de Leyes Sociales (fecha_pago)**
  - **Banco de Depósito de Leyes Sociales (banco_deposito)**

- Modifies the payslip report to:
  - Remove the message "Este recibo de nómina no es válido"
  - Eliminate the "Persona a Cargo" section
  - Remove the "Estado Civil" section
  - Exclude the "Calculado en" information

## Installation

1. Clone the repository to your Odoo addons directory.
2. Update the app list in Odoo.
3. Install the Custom Payslip Report module from the Odoo apps interface.

## Usage

Once installed, the module will automatically extend the payslip functionality. Users can access the new fields and modified report directly from the payslip interface.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.