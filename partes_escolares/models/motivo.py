from odoo import models, fields

class MotivoParte(models.Model):
    _name = 'instituto.motivo'
    _description = 'Motivos de los Partes'

    name = fields.Char(string='Descripción del Motivo', required=True)
    
    # Campo para medir en gráficas y pivot
    motivo_count = fields.Integer(default=1, string="Contador Motivos")
    
    # Esta relación es obligatoria para que el XML no dé error
    parte_ids = fields.One2many('instituto.parte', 'motivo_id', string='Partes con este motivo')