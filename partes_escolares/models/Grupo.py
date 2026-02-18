from odoo import models, fields

class Grupo(models.Model):
    _name = 'instituto.grupo'
    _description = 'Gestión de Grupos'

    name = fields.Char(string='Nombre del Grupo', required=True)
    grupo_count = fields.Integer(default=1, string="Contador Grupos")
    alumno_ids = fields.One2many('instituto.alumno', 'grupo_id', string='Alumnos')
    tutor_id = fields.Many2one('instituto.profesor', string='Tutor',required=True)
    asignatura_ids = fields.Many2many('instituto.asignatura', string='Asignaturas') #?
    _sql_constraints = [
        ('unique_profesor_grupo', 
         'unique(profesor_id)', 
         '¡Un profesor solo puede tener un grupo asignado!')
    ]