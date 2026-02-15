from odoo import models, fields

class Grupo(models.Model):
    _name = 'instituto.grupo'
    _description = 'Gestión de Grupos'

    name = fields.Char(string='Nombre del Grupo', required=True)
    alumno_ids = fields.One2many('instituto.alumno', 'grupo_id', string='Alumnos')
    profesor_ids = fields.Many2many(
        'instituto.profesor', 
        string='Profesores del Grupo',
        relation='instituto_profesor_grupo_rel'
    )

    def action_print_grupo(self):
        '''Imprime el reporte QWeb de la ficha del grupo.'''
        self.ensure_one()
        return self.env.ref('partes_escolares.action_report_grupo').report_action(self)