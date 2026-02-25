from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    profesor_id = fields.One2many(
        'instituto.profesor', 
        'user_id', 
        string='Profesor Vinculado'
    )
