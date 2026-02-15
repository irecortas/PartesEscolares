from odoo import models, fields, api

class MotivoParte(models.Model):
    _name = 'instituto.motivo'
    _description = 'Motivos de los Partes'

    name = fields.Char(string='Descripción del Motivo', required=True)
    
    # Esta relación es obligatoria para que el XML no dé error
    parte_ids = fields.One2many('instituto.parte', 'motivo_id', string='Partes con este motivo')

    partes_count = fields.Integer(string='Nº de Partes', compute='_compute_partes_count')

    @api.depends('parte_ids')
    def _compute_partes_count(self):
        for record in self:
            record.partes_count = len(record.parte_ids)

    def action_print_motivo(self):
        '''Imprime el reporte QWeb del motivo.'''
        self.ensure_one()
        return self.env.ref('partes_escolares.action_report_motivo').report_action(self)