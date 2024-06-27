from odoo import fields, models, api
from odoo.exceptions import AccessError
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    approval_request_id = fields.Many2one('approval.request', string="Request ID")
    approver_ids = fields.One2many(related='approval_request_id.approver_ids', string="Approvers", readonly=True)
    current_user_name = fields.Char(string="Current User", compute='_compute_current_user_name')
    current_user_status = fields.Char(string="Your Approval Status", compute='_compute_current_user_name')
    #approval_request_status = fields.Selection(string="Approval Request Status", related='approval_request_id.request_status', readonly=True)
    approval_request_status = fields.Char(string="Approval Request Status",  compute='_compute_current_status', readonly=True)


    @api.depends('approver_ids')
    def _compute_current_user_name(self):
        for order in self:
            current_user = self.env.user
            approver = order.approver_ids.filtered(lambda r: r.user_id == current_user)
            if approver:
                order.current_user_name = current_user.name
                order.current_user_status = approver.status
            else:
                order.current_user_name = 'not authorized'
                if order.approval_request_status != 'approved':
                    order.current_user_status ='Waiting Approvers Approvals'
                else:
                    order.current_user_status ='Approved'

    @api.depends('approver_ids')
    def _compute_current_status(self):
        for order in self:
            status=order.approval_request_id.request_status
            if status == 'approved'or status == 'refused' :
                order.approval_request_status=status
            else:
                order.approval_request_status="Waiting Approvers Approvals"

    @api.model
    def send_activity_message(self, user_ids, subject, note,res_id):
        activity_ids = []
        for user_id in user_ids:
            activity = self.env['mail.activity'].create({
                'res_model_id': self.env.ref('purchase.order'),
                'res_id': res_id,  # Set the ID of the record you want to associate the activity with
                'user_id': user_id,
                'summary': subject,
                'note': note,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,  # Assuming it's a to-do activity
            })
            activity_ids.append(activity.id)
        return activity_ids
    @api.model
    def notification(self,user_id,contract):
        
        activity_type = self.env.ref('inspire_approval.mail_act_activity')
        todos = {
        'res_id': contract.id,
        'res_model_id': self.env['ir.model'].search([('model', '=', 'purchase.order')]).id,
        'user_id': user_id,
        'summary': 'Approval Request',
        'note': 'There are an Approvals request waiting your approval',
        'activity_type_id': activity_type.id,
        'date_deadline': fields.date.today(),
        }
        self.env['mail.activity'].with_user(user_id).create(todos)

    def grant_approval(self):
        for order in self:
            if order.current_user_name == self.env.user.name:
                # Perform actions to grant approval here
                # For example:
                print('approved')
            else:
                raise UserError("You are not authorized to grant approval for this order.")

class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
