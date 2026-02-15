from odoo import models, fields, api

class Alumno(models.Model):
    _name = 'instituto.alumno'
    _description = 'Alumnos'

    name = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos")
    matricula = fields.Char(string="Nº Matrícula")
    image_128 = fields.Image(string="Foto", max_width=128, max_height=128)
    grupo_id = fields.Many2one('instituto.grupo', string="Grupo")
    
    # Requisito para Graph/Pivot: campo de medida
    alumno_count = fields.Integer(string="Contador", compute="_compute_count", store=True)

    @api.depends('name')
    def _compute_count(self):
        for record in self:
            record.alumno_count = 1

    def action_print_alumno(self):
        '''Imprime el reporte QWeb de la ficha del alumno.'''
        self.ensure_one()
        return self.env.ref('partes_escolares.action_report_alumno').report_action(self)