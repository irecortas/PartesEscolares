from odoo import fields, models, api

class Reportes(models.Model):
    _name = "reportes"
    name = fields.Char(string="Nombre")