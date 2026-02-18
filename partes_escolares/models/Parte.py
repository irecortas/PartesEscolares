from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Parte(models.Model):
    _name = 'instituto.parte'
    _description = 'Partes de Disciplina'

    name = fields.Char(string='Nombre', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    grupo_id = fields.Many2one('instituto.grupo', string='Grupo', related='alumno_id.grupo_id', store=True)
    fecha_hora = fields.Datetime(string='Fecha y Hora', compute='_compute_fecha_hora', store=True)
    hora = fields.Float(string='Hora')
    motivo_id = fields.Many2one('instituto.motivo', string='Motivo', required=True)
    alumno_id = fields.Many2one('instituto.alumno', string='Alumno', required=True)
    
    profesor_id = fields.Many2one(
        'instituto.profesor', 
        string='Profesor',
        default=lambda self: self.env['instituto.profesor'].search([('user_id', '=', self.env.user.id)], limit=1)
    ) #?

    profesor_ids_del_grupo = fields.Many2many(
        'instituto.profesor', 
        compute='_compute_profesores_permitidos',
        string='Profesores Permitidos'
    )

    descripcion = fields.Text(string='Detalles adicionales')
    lugar_id = fields.Many2one('instituto.lugar', string='Lugar')
    acciones = fields.Text(string='Acciones tomadas')
    prioridad = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
    ], string='Prioridad', default='0')
    state = fields.Selection([
        ('pendiente', 'Pendiente de contactar'),
        ('contactado', 'Contactado'),
        ('cerrado', 'Cerrado'),
    ], string='Estado', default='pendiente')
    incidencia_count = fields.Integer(default=1, string="Contador Incidencias")

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
                raise ValidationError("Debe seleccionar un profesor.")
            if record.fecha and record.fecha > fields.Date.today():
                raise ValidationError("La fecha del parte no puede ser futura.")

    @api.depends('fecha', 'hora')
    def _compute_fecha_hora(self):
        for record in self:
            if record.fecha and record.hora:
                try:
                    # Odoo stores Datetime in UTC. 
                    hour = int(record.hora)
                    minute = int((record.hora - hour) * 60)
                    dt_str = f"{record.fecha} {hour:02d}:{minute:02d}:00"
                    record.fecha_hora = fields.Datetime.from_string(dt_str)
                except Exception:
                    record.fecha_hora = False
            else:
                record.fecha_hora = False

    def action_pendiente(self):
        self.write({'state': 'pendiente'})

    def action_contactado(self):
        self.write({'state': 'contactado'})

    def action_cerrado(self):
        self.write({'state': 'cerrado'})
