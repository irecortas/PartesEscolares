from odoo import models, fields, api

class WizardSeleccionarAlumno(models.TransientModel):
    _name = 'instituto.wizard.seleccionar.alumno'
    _description = 'Asistente para Seleccionar Alumno'

    parte_id = fields.Many2one('instituto.parte', string='Parte', required=True)
    alumno_id = fields.Many2one('instituto.alumno', string='Seleccionar Alumno', required=True)

    def action_confirmar(self):
        self.ensure_one()
        self.parte_id.write({'alumno_id': self.alumno_id.id})
        return {'type': 'ir.actions.act_window_close'}
