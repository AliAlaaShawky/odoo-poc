
from odoo import models, fields ,api
from odoo.exceptions import ValidationError 
from datetime import datetime
class OrderType(models.Model):
    _name='order.type'
    name=fields.Char(required=True ,size=30)
    approval_scenario=fields.Many2one('approval.category',string="Approval Scenario",required=True )
    responsible=fields.Many2one('res.partner',string="Responsible",required=True)
    Description=fields.Text()
    