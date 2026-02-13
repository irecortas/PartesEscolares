from odoo import models, fields

class Grupo(models.Model):
    _name = 'instituto.grupo'
    _description = 'Gestión de Grupos'

    name = fields.Char(string='Nombre del Grupo', required=True)
    grupo_count = fields.Integer(default=1, string="Contador Grupos") # Necesario para Graph
    alumno_ids = fields.One2many('instituto.alumno', 'grupo_id', string='Alumnos')
    profesor_ids = fields.Many2many('instituto.profesor', string='Profesores del Grupo')