from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import lxml.etree as etree
import logging

_logger = logging.getLogger(__name__)

class XmlImportWizard(models.TransientModel):
    _name = 'xml.import.wizard'
    _description = 'Wizard Importador de Datos'

    xml_file = fields.Binary(string='Archivo XML', required=True)
    file_name = fields.Char(string='Nombre del archivo')
    tipo_importacion = fields.Selection([
        ('profesores', 'Profesores'),
        ('grupos', 'Grupos'),
        ('alumnos', 'Alumnos')
    ], string='Tipo de Importación', required=True)

    def action_import_xml(self):
        self.ensure_one()
        if not self.xml_file:
            raise UserError(_("Por favor, seleccione un archivo XML."))

        xml_content = base64.b64decode(self.xml_file)
        try:
            root = etree.fromstring(xml_content)
        except Exception as e:
            _logger.error("Error parseando XML: %s", str(e))
            raise UserError(_("Error al leer el archivo XML: %s") % str(e))

        # --- PROFESORES ---
        if self.tipo_importacion == 'profesores':
            docentes = root.xpath('//docente')
            for d in docentes:
                dni = d.get('documento')
                if dni:
                    existente = self.env['instituto.profesor'].search([('cedula', '=', dni)], limit=1)
                    if not existente:
                        self.env['instituto.profesor'].create({
                            'name': f"{d.get('nombre')} {d.get('apellido1')} {d.get('apellido2') or ''}".strip(),
                            'cedula': dni,
                            'email': d.get('email1'),
                            # Estos campos requieren que existan en el modelo
                            # 'domicilio': d.get('domicilio'),
                            # 'telefono1': d.get('telefono1'),
                        })

        # --- GRUPOS ---
        elif self.tipo_importacion == 'grupos':
            grupos = root.xpath('//grupo')
            for g in grupos:
                codigo = g.get('codigo')
                if codigo:
                    existente = self.env['instituto.grupo'].search([('name', '=', codigo)], limit=1)
                    if not existente:
                        tutor_dni = g.get('tutor_ppal')
                        tutor = self.env['instituto.profesor'].search([('cedula', '=', tutor_dni)], limit=1)
                        
                        # Si no hay tutor, buscamos el primero disponible (tutor_id es obligatorio en el modelo)
                        if not tutor:
                            tutor = self.env['instituto.profesor'].search([], limit=1)
                        
                        if not tutor:
                            raise UserError(_("No hay profesores para asignar como tutor al grupo %s") % codigo)

                        self.env['instituto.grupo'].create({
                            'name': codigo,
                            'denominacion': g.get('nombre'),
                            'aula': g.get('aula').strip() if g.get('aula') else '',
                            'tutor_id': tutor.id,
                        })

        # --- ALUMNOS ---
        elif self.tipo_importacion == 'alumnos':
            alumnos = root.xpath('//alumno')
            for a in alumnos:
                nia = a.get('NIA')
                if nia:
                    existente = self.env['instituto.alumno'].search([('nia', '=', nia)], limit=1)
                    if not existente:
                        cod_grupo = a.get('grupo')
                        grupo = self.env['instituto.grupo'].search([('name', '=', cod_grupo)], limit=1)
                        
                        vals = {
                            'name': a.get('nombre') or 'Sin nombre',
                            'apellidos': f"{a.get('apellido1')} {a.get('apellido2') or ''}".strip(),
                            'nia': nia,
                            'matricula': a.get('documento'), # Usamos documento como matrícula si no hay campo dni
                        }
                        if grupo:
                            vals['grupo_ids'] = [(6, 0, [grupo.id])]
                        
                        self.env['instituto.alumno'].create(vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Éxito'),
                'message': _('Datos importados correctamente'),
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'},
            }
        }
