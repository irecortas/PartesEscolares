from odoo import models, fields, api

class Alumno(models.Model):
    _name = 'instituto.alumno'
    _description = 'Registro de Alumnos'

    name = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    matricula = fields.Char(string='Matrícula')
    nia = fields.Char(string='NIA')
    grupo_id = fields.Many2one('instituto.grupo', string='Grupo')
    parte_ids = fields.One2many('instituto.parte', 'alumno_id', string='Partes')
    partes_activas = fields.Integer(string='Partes Activas', compute='_compute_partes_activas')

    @api.depends('parte_ids.state')
    def _compute_partes_activas(self):
        for record in self:
            record.partes_activas = len([p for p in record.parte_ids if p.state != 'cerrado'])
