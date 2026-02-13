from odoo import models, fields

class Alumno(models.Model):
    _name = 'instituto.alumno'
    _description = 'Registro de Alumnos'

    name = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    matricula = fields.Char(string='Matrícula')
    # Campo para la foto en el Kanban
    image_128 = fields.Image(string="Foto", max_width=128, max_height=128)
    # Campo para medir en gráficas y pivot
    alumno_count = fields.Integer(default=1, string="Contador Alumnos")
    
    grupo_id = fields.Many2one('instituto.grupo', string='Grupo')
    parte_ids = fields.One2many('instituto.parte', 'alumno_id', string='Partes')

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.matricula or 'S/M'}] {record.name} {record.apellidos}"
            result.append((record.id, name))
        return result