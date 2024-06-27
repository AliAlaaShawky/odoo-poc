# -*- coding: utf-8 -*-
# from odoo import http


# class InspireApproval(http.Controller):
#     @http.route('/inspire_approval/inspire_approval', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inspire_approval/inspire_approval/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inspire_approval.listing', {
#             'root': '/inspire_approval/inspire_approval',
#             'objects': http.request.env['inspire_approval.inspire_approval'].search([]),
#         })

#     @http.route('/inspire_approval/inspire_approval/objects/<model("inspire_approval.inspire_approval"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inspire_approval.object', {
#             'object': obj
#         })

