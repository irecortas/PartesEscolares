from odoo import models, fields, api

class Alumno(models.Model):
    _name = 'instituto.alumno'
    _description = 'Registro de Alumnos'
    _rec_name = 'name'

    name = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    matricula = fields.Char(string='Matrícula')
    nia = fields.Char(string='NIA')
    grupo_ids = fields.Many2many('instituto.grupo', string='Grupos')
    parte_ids = fields.One2many('instituto.parte', 'alumno_id', string='Partes')
    partes_activas = fields.Integer(string='Partes Activas', compute='_compute_partes_activas')

    @api.depends('parte_ids.state')
    def _compute_partes_activas(self):
        for record in self:
            record.partes_activas = len([p for p in record.parte_ids if p.state != 'cerrado'])

    def name_get(self):
        result = []
        for record in self:
            nombre_completo = record.name
            if record.apellidos:
                nombre_completo = f"{record.name} {record.apellidos}"
            result.append((record.id, nombre_completo))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            domain = ['|', ('name', operator, name), ('apellidos', operator, name)]
        else:
            domain = []
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
