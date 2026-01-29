from odoo import fields, models, api

class Profesor(models.Model):
    _name = 'instituto.profesor'
    _description = 'Registro de Profesores'

    name = fields.Char(string='Nombre del Profesor', required=True)
    especialidad = fields.Char(string='Especialidad')
    
    # RELACIÓN: Muchos profesores pueden estar en muchos grupos
    # Odoo crea automáticamente la tabla intermedia 'instituto_profesor_grupo_rel'
    grupo_ids = fields.Many2many(
        'instituto.grupo', 
        string='Grupos Asignados',
        relation='instituto_profesor_grupo_rel'
    )