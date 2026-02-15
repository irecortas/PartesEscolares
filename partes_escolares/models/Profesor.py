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
    user_id = fields.Many2one('res.users', string='Usuario de Odoo', help="Usuario vinculado a este profesor")
    grupo_ids = fields.Many2many(
        'instituto.grupo', 
        string='Grupos Asignados',
        relation='instituto_profesor_grupo_rel'
    )

    parte_ids = fields.One2many('instituto.parte', 'profesor_id', string='Partes Emitidos')

    def action_print_profesor(self):
        '''Imprime el reporte QWeb de la ficha del profesor.'''
        self.ensure_one()
        return self.env.ref('partes_escolares.action_report_profesor').report_action(self)