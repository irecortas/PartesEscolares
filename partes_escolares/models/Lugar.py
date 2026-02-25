from odoo import models, fields

class Lugar(models.Model):
    _name = 'instituto.lugar'
    _description = 'Lugar'

    name = fields.Char(string='Nombre del lugar', required=True)
    parte_ids = fields.One2many('instituto.parte', 'lugar_id', string='Partes Emitidos')