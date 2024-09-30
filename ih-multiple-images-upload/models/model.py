
from odoo import models
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_context(self):
        # Example of setting the flag for multiple image uploads
        return {
            'isProductMultipleImagesUpload': True,
        }