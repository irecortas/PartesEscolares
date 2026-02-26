from odoo import models, fields

class Aula(models.Model):
    _name = 'instituto.aula'
    _description = 'Aula'

    name = fields.Char(string='Nombre de la aula', required=True)
    planta = fields.Integer(string='Planta', required=True)
    edificio = fields.Char(string='Edificio', required=True)
    
    aula_count = fields.Integer(default=1, string="Contador aulas")

    parte_ids = fields.One2many('instituto.parte', 'lugaraula_id', string='Partes con esta aula')