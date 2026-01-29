from odoo import models, fields

class Grupo(models.Model):
    _name = 'instituto.grupo'
    _description = 'Gestión de Grupos'

    name = fields.Char(string='Nombre del Grupo', required=True)
    alumno_ids = fields.One2many('instituto.alumno', 'grupo_id', string='Alumnos')
    profesor_ids = fields.Many2many('instituto.profesor', string='Profesores')