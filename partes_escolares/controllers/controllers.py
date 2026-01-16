# -*- coding: utf-8 -*-
# from odoo import http


# class PartesEscolares(http.Controller):
#     @http.route('/partes_escolares/partes_escolares/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partes_escolares/partes_escolares/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partes_escolares.listing', {
#             'root': '/partes_escolares/partes_escolares',
#             'objects': http.request.env['partes_escolares.partes_escolares'].search([]),
#         })

#     @http.route('/partes_escolares/partes_escolares/objects/<model("partes_escolares.partes_escolares"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partes_escolares.object', {
#             'object': obj
#         })
