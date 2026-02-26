from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class Parte(models.Model):
    _name = 'instituto.parte'
    _description = 'Partes de Disciplina'

    name = fields.Char(string='Nombre', required=True, copy=False, default='/')
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today, required=True)
    grupo_id = fields.Many2one('instituto.grupo', string='Grupo', required=True)
    fecha_hora = fields.Datetime(string='Fecha y Hora', compute='_compute_fecha_hora', store=True)
    hora = fields.Float(string='Hora', required=True)
    motivo_id = fields.Many2one('instituto.motivo', string='Motivo', required=True)
    alumno_id = fields.Many2one('instituto.alumno', string='Alumno', required=True)
    asignatura_id = fields.Many2one('instituto.asignatura', string='Asignatura', required=True)

    profesor_id = fields.Many2one(
        'instituto.profesor', 
        string='Profesor',
        required=True,
        default=lambda self: self.env['instituto.profesor'].search([('user_id', '=', self.env.user.id)], limit=1)
    )

    descripcion = fields.Text(string='Detalles adicionales')
    aula_id = fields.Many2one('instituto.aula', string='Aula', required=True)
    acciones = fields.Text(string='Acciones tomadas')
    state = fields.Selection([
        ('pendiente', 'Pendiente de contactar'),
        ('contactado', 'Contactado'),
        ('cerrado', 'Cerrado'),
    ], string='Estado', default='pendiente')
    incidencia_count = fields.Integer(default=1, string="Contador Incidencias")

    # Cambiamos es_admin a un campo normal para que Odoo lo pase bien al frontend en el create
    es_admin = fields.Boolean(
        string='Es Administrador',
        default=lambda self: self.env.user.has_group('partes_escolares.group_instituto_admin')
    )

    @api.model
    def default_get(self, fields_list):
        res = super(Parte, self).default_get(fields_list)
        # Aseguramos que es_admin se pase siempre
        res['es_admin'] = self.env.user.has_group('partes_escolares.group_instituto_admin')
        
        if 'name' in fields_list or not res.get('name') or res.get('name') == '/':
            count = self.env['instituto.parte'].search_count([]) + 1
            res['name'] = f"Parte {count}"
        return res

    @api.onchange('alumno_id')
    def _onchange_alumno_id(self):
        if self.alumno_id and self.alumno_id.grupo_ids:
            self.grupo_id = self.alumno_id.grupo_ids[0].id
        elif not self.alumno_id:
            self.grupo_id = False

    @api.constrains('profesor_id', 'alumno_id', 'fecha')
    def _check_validez(self):
        for record in self:
            if not record.profesor_id:
                raise ValidationError("Debe seleccionar un profesor.")
            if record.fecha and record.fecha > fields.Date.today():
                raise ValidationError("La fecha del parte no puede ser futura.")
            
            if not record.env.user.has_group('partes_escolares.group_instituto_admin'):
                current_profesor = record.env['instituto.profesor'].search(
                    [('user_id', '=', record.env.user.id)], limit=1
                )
                if current_profesor and record.profesor_id != current_profesor:
                    raise ValidationError(_("Solo puedes crear partes con tu propio nombre de profesor."))

    @api.depends('fecha', 'hora')
    def _compute_fecha_hora(self):
        for record in self:
            if record.fecha and record.hora is not False:
                try:
                    hour = int(record.hora)
                    minute = int(round((record.hora - hour) * 60))
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
