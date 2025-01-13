.. |company| replace:: OnlyOne 

   :alt: 
   :target: https://www.onlyone.odoo:com

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==============
Funcionalidades del Módulo de Localización Argentina para HR Employee
==============

Este módulo extiende las funcionalidades del modelo `hr.employee` en Odoo, incorporando información específica para la localización Argentina y optimizando las vistas de formulario, kanban y lista.

## Características Principales

### 1. **Extensión de la Vista de Formulario**
Se añade una nueva página en el cuaderno de información del empleado, llamada "Localización Argentina", con los siguientes grupos:

#### Información Básica
- **Legajo**: Número de identificación del empleado.
- **Código de revista**: Clasificación laboral del empleado.
- **Convenio**: Selección del convenio colectivo aplicable (sin opción de abrir desde aquí).
- **Categoría**: Nivel laboral del empleado dentro del convenio.
- **Sindicado**: Indicador de afiliación sindical.
- **Sindicato**: Sindicato al que pertenece el empleado.
- **Compañía aseguradora**: Entidad de ART (Aseguradora de Riesgos del Trabajo).
- **Obra social**: Obra social asignada al empleado (sin opción de abrir desde aquí).

#### Información Laboral
- **Fecha de egreso**: Fecha de desvinculación del empleado.
- **Fecha de accidente**: Fecha del último accidente reportado.
- **Jornada laboral**: Tipo de jornada laboral (completa, parcial, etc.).
- **Estado**: Estatus laboral (solo lectura).

### 2. **Nueva Vista Kanban Extendida**
Se introduce una nueva vista Kanban optimizada con los siguientes campos adicionales:

#### Campos
- **Días de ausencia**: Cantidad de días que el empleado estuvo ausente.
- **Días de accidente**: Días de baja laboral debido a accidentes.
- **Cantidad de sanciones**: Total de sanciones registradas.

#### Plantilla de Tarjetas
Cada tarjeta muestra:
- Nombre del empleado.
- Puesto y departamento (si están disponibles).
- Indicadores clave:
  - Días ausentes (resaltado en rojo).
  - Días de accidente (resaltado en amarillo).
  - Sanciones (resaltado en rojo).

### 3. **Extensión de la Vista de Lista**
Se añaden tres nuevos campos a la vista de lista de empleados, después del correo electrónico laboral:
- **Días de ausencia**.
- **Días de accidente**.
- **Cantidad de sanciones**.

## Beneficios
- **Adaptación Local**: Integra información específica para la gestión de empleados en Argentina.
- **Mayor Visibilidad**: Presenta indicadores clave en vistas kanban y lista, facilitando la gestión del personal.
- **Organización Mejorada**: Centraliza información laboral crítica en un único lugar accesible.

## Configuración
- **Instalación del Módulo**: El módulo debe estar instalado en un sistema Odoo compatible con el módulo base de Recursos Humanos (`hr`).
- **Requisitos**:
  - Módulo base `hr`.
  - Información de los empleados cargada previamente.

## Uso
1. Accede al menú de empleados.
2. Abre la ficha de un empleado.
3. Revisa la página "Localización Argentina" para gestionar la información laboral y sindical.
4. Utiliza la vista kanban para obtener una visión rápida de indicadores clave como ausencias, accidentes y sanciones.
5. Consulta la vista de lista para analizar los mismos indicadores en formato tabular.


## Créditos

### Imágenes

* |company| |icon|

### Contribuidores

### Mantenedor

|company_logo|

Este módulo es mantenido por la |company|. Es ideal para empresas que operan en Argentina y necesitan manejar información específica relacionada con la legislación laboral y sindical del país.

