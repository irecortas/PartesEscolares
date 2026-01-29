from odoo import models, fields, api

class Parte(models.Model):
    _name = 'instituto.parte'
    _description = 'Partes de Disciplina'

    name = fields.Char(string='Folio', default='Nuevo', readonly=True)
    descripcion = fields.Text(string='Motivo del Parte')
    
    # --- ESTOS SON LOS CAMPOS QUE TE FALTAN ---
    fecha = fields.Date(string='Fecha', default=fields.Date.context_today)
    
    tipo_parte = fields.Selection([
        ('leve', 'Leve'),
        ('grave', 'Grave'),
        ('muy_grave', 'Muy Grave')
    ], string='Tipo de Parte', default='leve')
    
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('firmado', 'Firmado'),
        ('cerrado', 'Cerrado')
    ], string='Estado', default='borrador')
    # ------------------------------------------

    alumno_id = fields.Many2one('instituto.alumno', string='Alumno', required=True)
    profesor_id = fields.Many2one('instituto.profesor', string='Profesor', required=True)
    grupo_id = fields.Many2one('instituto.grupo', string='Grupo', related='alumno_id.grupo_id', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('instituto.parte') or 'PARTE-001'
        return super(Parte, self).create(vals)