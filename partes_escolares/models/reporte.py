from odoo import fields, models, api

class Reportes(models.Model):
    _name = "instituto.reporte"
    name = fields.Char()