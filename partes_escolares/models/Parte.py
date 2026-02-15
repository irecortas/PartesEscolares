from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Parte(models.Model):
    _name = 'instituto.parte'
    _description = 'Partes de Disciplina'

    name = fields.Char(string='Nombre', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today, readonly=True)
    motivo_id = fields.Many2one('instituto.motivo', string='Motivo', required=True)

    alumno_id = fields.Many2one('instituto.alumno', string='Alumno', required=True)
    grupo_id = fields.Many2one(
        'instituto.grupo', 
        string='Grupo', 
        related='alumno_id.grupo_id', 
        store=True
    )
    
    profesor_id = fields.Many2one(
        'instituto.profesor', 
        string='Profesor',
        default=lambda self: self.env['instituto.profesor'].search([('user_id', '=', self.env.user.id)], limit=1)
    )

    profesor_ids_del_grupo = fields.Many2many(
        'instituto.profesor', 
        compute='_compute_profesores_permitidos',
        string='Profesores Permitidos'
    )

    descripcion = fields.Text(string='Detalles adicionales')

    estado = fields.Selection([
        ('pendiente', 'Pendiente de contactar'),
        ('contactado', 'Contactado'),
        ('cerrado', 'Cerrado')
    ], string='Estado', default='pendiente')

    # CAMPO PARA GRÁFICOS (REQUISITO PDF)
    incidencia_count = fields.Integer(string="Cantidad", default=1, readonly=True)

    @api.depends('alumno_id')
    def _compute_profesores_permitidos(self):
        for record in self:
            if record.alumno_id and record.alumno_id.grupo_id:
                record.profesor_ids_del_grupo = record.alumno_id.grupo_id.profesor_ids
            else:
                record.profesor_ids_del_grupo = self.env['instituto.profesor'].search([])

    @api.constrains('profesor_id', 'alumno_id', 'fecha')
    def _check_validez(self):
        for record in self:
            if not record.profesor_id:
                raise ValidationError("Debe seleccionar un profesor para crear el parte.")
            if record.fecha and record.fecha > fields.Date.today():
                raise ValidationError("La fecha del parte no puede ser futura.")

    def action_print_parte(self):
        '''Acción para imprimir el reporte QWeb del parte actual.'''
        self.ensure_one()
        return self.env.ref('partes_escolares.action_report_parte').report_action(self)