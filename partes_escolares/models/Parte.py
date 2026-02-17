from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Parte(models.Model):
    _name = 'instituto.parte'
    _description = 'Partes de Disciplina'

    name = fields.Char(string='Nombre', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    hora = fields.Char(string='Hora')
    motivo_id = fields.Many2one('instituto.motivo', string='Motivo', required=True)
    alumno_id = fields.Many2one('instituto.alumno', string='Alumno', required=True)
    grupo_id = fields.Many2one('instituto.grupo', string='Grupo', related='alumno_id.grupo_id', store=True)
    

    profesor_id = fields.Many2one(
        'instituto.profesor', 
        string='Profesor',
        default=lambda self: self.env['instituto.profesor'].search([('user_id', '=', self.env.user.id)], limit=1)
    )

    # --- ESTO ES LO QUE FALTABA (EL CAMPO QUE EL XML BUSCA) ---
    profesor_ids_del_grupo = fields.Many2many(
        'instituto.profesor', 
        compute='_compute_profesores_permitidos',
        string='Profesores Permitidos'
    )

    descripcion = fields.Text(string='Detalles adicionales')
    lugar_id = fields.Many2one('instituto.lugar', string='Lugar')
    situacion_id = fields.Many2one('instituto.situacion', string='Situación', default=lambda self: self.env['instituto.situacion'].search([('name', '=', 'Pendiente de contactar')], limit=1))
    situacion_name = fields.Char(related='situacion_id.name', string='Nombre Situación', store=True)
    prioridad = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
    ], string='Prioridad', default='0')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('open', 'Abierto'),
        ('in_progress', 'En Progreso'),
        ('done', 'Cerrado'),
    ], string='Estado', default='draft', tracking=True)
    incidencia_count = fields.Integer(default=1, string="Contador Incidencias")

    @api.depends('alumno_id')
    def _compute_profesores_permitidos(self):
        for record in self:
            if record.alumno_id and record.alumno_id.grupo_id:
                # Asignamos los IDs de los profesores asociados al grupo
                record.profesor_ids_del_grupo = record.alumno_id.grupo_id.profesor_ids
            else:
                # Si no hay alumno seleccionado, permitimos todos los profesores
                record.profesor_ids_del_grupo = self.env['instituto.profesor'].search([])


    @api.constrains('profesor_id', 'alumno_id', 'fecha')
    def _check_validez(self):
        for record in self:
            if not record.profesor_id:
                raise ValidationError("Debe seleccionar un profesor.")
            if record.fecha and record.fecha > fields.Date.today():
                raise ValidationError("La fecha del parte no puede ser futura.")

    def action_confirm(self):
        self.write({'state': 'open'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_reset(self):
        self.write({'state': 'draft'})
