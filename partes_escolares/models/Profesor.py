from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'instituto.profesor'
    _description = 'Registro de Profesores'

    name = fields.Char(string='Nombre del Profesor', required=True)
    especialidad = fields.Char(string='Especialidad')
    
    cedula = fields.Char(string='Cédula/DNI')
    email = fields.Char(string='Correo Electrónico') 

    profesor_count = fields.Integer(default=1, string="Contador Profesores")

    user_id = fields.Many2one('res.users', string='Usuario de Odoo', help="Usuario vinculado a este profesor") #?

    parte_ids = fields.One2many('instituto.parte', 'profesor_id', string='Partes Emitidos')
    grupo_id = fields.One2many('instituto.grupo', 'tutor_id', string='Grupo Tutorizado',limit=1 )
    asignatura_ids = fields.Many2many('instituto.asignatura', string='Asignaturas') #?
    grupo_ids = fields.Many2many('instituto.grupo', string='Grupos que imparte')