from odoo import models, fields

class Situacion(models.Model):
    _name = 'instituto.situacion'
    _description = 'Situaciones de Partes'

    name = fields.Char(string='Nombre de la Situación', required=True)