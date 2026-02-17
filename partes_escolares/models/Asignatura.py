from odoo import models, fields

class Asignatura(models.Model):
    _name = 'instituto.asignatura'
    _description = 'Asignaturas'

    name = fields.Char(string='Nombre de la Asignatura', required=True)
    profesor_ids = fields.Many2many('instituto.profesor', string='Profesores')
    grupo_ids = fields.Many2many('instituto.grupo', string='Grupos')