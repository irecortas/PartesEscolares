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

    grupo_ids = fields.Many2many(
        'instituto.grupo', 
        string='Grupos Asignados',
        relation='instituto_profesor_grupo_rel'
    )