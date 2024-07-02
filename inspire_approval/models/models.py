from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    allow_product_domain_id_ids=fields.Many2many('product.template',compute='allow_product_domain_ids')
    @api.onchange('partner_id')
    def allow_product_domain_ids(self):
        for rec in self:
         all_vendor = self.env['product.template'].search([('seller_ids.partner_id', '=', rec.partner_id.id)])
         rec.allow_product_domain_id_ids=[(6,0,all_vendor.ids)]









