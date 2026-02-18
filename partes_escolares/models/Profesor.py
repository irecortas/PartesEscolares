from odoo import models, fields

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

    @api.depends('grupo_id')
    def _compute_grupo_actual(self):
        for profesor in self:
            profesor.grupo_actual_id = profesor.grupo_id[:1].id if profesor.grupo_id else False