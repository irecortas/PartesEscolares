from odoo import models, fields

class MotivoParte(models.Model):
    _name = 'instituto.motivo'
    _description = 'Motivos de los Partes'

    name = fields.Char(string='Descripción del Motivo', required=True)
    
    # Esta relación es obligatoria para que el XML no dé error
    parte_ids = fields.One2many('instituto.parte', 'motivo_id', string='Partes con este motivo')