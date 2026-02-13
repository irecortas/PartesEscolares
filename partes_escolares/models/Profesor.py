from odoo import models, fields

class Profesor(models.Model):
    _name = 'instituto.profesor'
    _description = 'Registro de Profesores'

    name = fields.Char(string='Nombre del Profesor', required=True)
    especialidad = fields.Char(string='Especialidad')
    
    # --- AÑADE ESTOS CAMPOS ---
    cedula = fields.Char(string='Cédula/DNI')
    email = fields.Char(string='Correo Electrónico')
    # --------------------------
    # Campo para medir en gráficas y pivot
    profesor_count = fields.Integer(default=1, string="Contador Profesores")

    user_id = fields.Many2one('res.users', string='Usuario de Odoo', help="Usuario vinculado a este profesor")
    grupo_ids = fields.Many2many(
        'instituto.grupo', 
        string='Grupos Asignados',
        relation='instituto_profesor_grupo_rel'
    )

    parte_ids = fields.One2many('instituto.parte', 'profesor_id', string='Partes Emitidos')