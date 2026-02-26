from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Profesor(models.Model):
    _name = 'instituto.profesor'
    _description = 'Registro de Profesores'

    name = fields.Char(string='Nombre del Profesor', required=True)
    # especialidad = fields.Char(string='Especialidad')
    
    cedula = fields.Char(string='Cédula/DNI')
    email = fields.Char(string='Correo Electrónico') 

    profesor_count = fields.Integer(default=1, string="Contador Profesores")
    
    user_role = fields.Selection([
        ('profesor', 'Profesor'),
        ('tutor', 'Tutor'),
        ('admin', 'Administrador'),
    ], string='Rol para Nuevo Usuario', default='profesor', 
    help="Rol que se asignará al crear el usuario de Odoo")

    def action_create_user(self):
        self.ensure_one()
        if self.user_id:
            raise UserError(_("Este profesor ya tiene un usuario vinculado."))
        if not self.email:
            raise UserError(_("Se requiere un correo electrónico para crear el usuario."))
        
        # Determinar el grupo ID según el rol seleccionado
        group_ref = 'partes_escolares.group_instituto_profesor'
        if self.user_role == 'tutor':
            group_ref = 'partes_escolares.group_instituto_tutor'
        elif self.user_role == 'admin':
            group_ref = 'partes_escolares.group_instituto_admin'

        user_vals = {
            'name': self.name,
            'login': self.email,
            'email': self.email,
            'groups_id': [(6, 0, [self.env.ref(group_ref).id])]
        }
        user = self.env['res.users'].create(user_vals)
        self.user_id = user.id
        return True

    user_id = fields.Many2one('res.users', string='Usuario de Odoo', help="Usuario vinculado a este profesor") 
    
    _sql_constraints = [
        ('user_id_unique', 'unique(user_id)', 'El usuario de Odoo ya está vinculado a otro profesor.')
    ]

    parte_ids = fields.One2many('instituto.parte', 'profesor_id', string='Partes Emitidos')
    grupo_tutorizado_ids = fields.One2many('instituto.grupo', 'tutor_id', string='Grupos Tutorizados')
    asignatura_ids = fields.Many2many('instituto.asignatura', string='Asignaturas') #?
