from odoo import models, fields

class Lugar(models.Model):
    _name = 'instituto.lugar'
    _description = 'Lugares'

    name = fields.Char(string='Nombre del Lugar', required=True)