from odoo import models, fields

class Alumno(models.Model):
    _name = 'instituto.alumno'
    _description = 'Registro de Alumnos'

    name = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    matricula = fields.Char(string='Matrícula')
    grupo_id = fields.Many2one('instituto.grupo', string='Grupo')
    parte_ids = fields.One2many('instituto.parte', 'alumno_id', string='Partes')