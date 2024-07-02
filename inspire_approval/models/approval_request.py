# from odoo import fields, models, api
# from odoo.exceptions import AccessError
# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
#     approval_request_id = fields.Many2one('approval.request', string="Request ID")
#     approver_ids = fields.One2many(related='approval_request_id.approver_ids', string="Approvers", readonly=True)
#     current_user_name = fields.Char(string="Current User", compute='_compute_current_user_name')
#     current_user_status = fields.Char(string="Your Approval Status", compute='_compute_current_user_name')
#     #approval_request_status = fields.Selection(string="Approval Request Status", related='approval_request_id.request_status', readonly=True)
#     approval_request_status = fields.Char(string="Approval Request Status",  compute='_compute_current_status', readonly=True)
#     order_type = fields.Many2one('order.type',string="Order Type", required=True)
#     approval_scenario_2=fields.Many2one('approval.category',string="Approval Scenario",related='order_type.approval_scenario', readonly=True)
#     @api.depends('approver_ids')
#     def _compute_current_user_name(self):
#         for order in self:
#             current_user = self.env.user
#             approver = order.approver_ids.filtered(lambda r: r.user_id == current_user)
#             if approver:
#                 order.current_user_name = current_user.name
#                 order.current_user_status = approver.status
#             else:
#                 order.current_user_name = 'not authorized'
#                 if order.approval_request_status != 'approved':
#                     order.current_user_status ='Waiting Approvers Approvals'
#                 else:
#                     order.current_user_status ='Approved'

#     @api.depends('approver_ids')
#     def _compute_current_status(self):
#         for order in self:
#             status=order.approval_request_id.request_status
#             if status == 'approved'or status == 'refused' :
#                 order.approval_request_status=status
#             else:
#                 order.approval_request_status="Waiting Approvers Approvals"

#     @api.model
#     def send_activity_message(self, user_ids, subject, note,res_id):
#         activity_ids = []
#         for user_id in user_ids:
#             activity = self.env['mail.activity'].create({
#                 'res_model_id': self.env.ref('purchase.order'),
#                 'res_id': res_id,  # Set the ID of the record you want to associate the activity with
#                 'user_id': user_id,
#                 'summary': subject,
#                 'note': note,
#                 'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,  # Assuming it's a to-do activity
#             })
#             activity_ids.append(activity.id)
#         return activity_ids
#     @api.model
#     def notification(self,user_id,contract):
        
#         activity_type = self.env.ref('inspire_approval.mail_act_activity')
#         todos = {
#         'res_id': contract.id,
#         'res_model_id': self.env['ir.model'].search([('model', '=', 'purchase.order')]).id,
#         'user_id': user_id,
#         'summary': 'Approval Request',
#         'note': 'There are an Approvals request waiting your approval',
#         'activity_type_id': activity_type.id,
#         'date_deadline': fields.date.today(),
#         }
#         self.env['mail.activity'].with_user(user_id).create(todos)

#     def grant_approval(self):
#         for order in self:
#             if order.current_user_name == self.env.user.name:
#                 # Perform actions to grant approval here
#                 # For example:
#                 print('approved')
#             else:
#                 raise UserError("You are not authorized to grant approval for this order.")

# class ApprovalRequest(models.Model):
#     _inherit = 'approval.request'

#     purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')


from odoo import fields, models, api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    approval_request_id = fields.Many2one('approval.request', string="Request ID")
    approver_ids = fields.One2many(related='approval_request_id.approver_ids', string="Approvers", readonly=True)
    current_user_name = fields.Char(string="Current User", compute='_compute_current_user_name')
    current_user_status = fields.Char(string="Your Approval Status", compute='_compute_current_user_name')
    approval_request_status = fields.Char(string="Approval Request Status", compute='_compute_current_status', readonly=True)
    order_type = fields.Many2one('order.type', string="Order Type", required=True)
    approval_scenario_2 = fields.Many2one('approval.category', string="Approval Scenario", related='order_type.approval_scenario', readonly=True)
    order_subject=fields.Text(sting="Description" , required=True)
    # Dummy translation function
    def _translate(self, text):
        translations = {
            'ar_001': {
                'not authorized': 'غير مصرح',
                'refused':'تم الرفض',
                'new':'جديد',
                'Waiting Approvers Approvals': 'في انتظار موافقة المراجعين',
                'approved': 'تمت الموافقة',
                'Approval Request': 'طلب الموافقة',
                'There are an Approvals request waiting your approval': 'هناك طلبات موافقة في انتظار موافقتك',
                'There are a purchase request waiting for you' :'هناك طلب شراء في انتظارك',
                'Purchase Request': 'طلب شراء',
                
            }
        }
        lang = self.env.user.lang
        return translations.get(lang, {}).get(text, text)

    @api.depends('approver_ids')
    def _compute_current_user_name(self):
        for order in self:
            current_user = self.env.user
            approver = order.approver_ids.filtered(lambda r: r.user_id == current_user)
            if approver:
                order.current_user_name = current_user.name
                order.current_user_status = self._translate(approver.status)
            else:
                order.current_user_name = self._translate('not authorized')
                if order.approval_request_status == 'approved':
                    order.current_user_status = self._translate('approved')
                elif order.approval_request_status == 'refused':
                    order.current_user_status = self._translate('refused')
                else:
                   order.current_user_status = self._translate('Waiting Approvers Approvals')

    @api.depends('approver_ids')
    def _compute_current_status(self):
        for order in self:
            status = order.approval_request_id.request_status
            if status in ['approved', 'refused']:
                order.approval_request_status = self._translate(status)
            else:
                order.approval_request_status = self._translate('Waiting Approvers Approvals')

    @api.model
    def send_activity_message(self, user_ids, subject, note, res_id):
        subject = self._translate(subject)
        note = self._translate(note)
        
        activity_ids = []
        for user_id in user_ids:
            activity = self.env['mail.activity'].create({
                'res_model_id': self.env.ref('purchase.order').id,
                'res_id': res_id,
                'user_id': user_id,
                'summary': subject,
                'note': note,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            })
            activity_ids.append(activity.id)
        return activity_ids

    @api.model
    def notification(self, user_id, contract):
        activity_type = self.env.ref('inspire_approval.mail_act_activity')
        summary = self._translate('Approval Request')
        note = self._translate('There are an Approvals request waiting your approval')
        
        todos = {
            'res_id': contract.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
            'user_id': user_id,
            'summary': summary,
            'note': note,
            'activity_type_id': activity_type.id,
            'date_deadline': fields.date.today(),
        }
        self.env['mail.activity'].with_user(user_id).create(todos)
    def grant_approval(self):
        for record in self:
            if record.approval_request_id:
                approval_request = record.approval_request_id
                current_user = self.env.user

                # Check if the current user is in the list of approvers of the approval category
                approvers = approval_request.category_id.approver_ids
                if current_user in approval_request.approver_ids.mapped('user_id'):
                
                    
                        approval_request.action_approve()
                        activity = self.env['mail.activity'].search([
                                ('res_id', '=', self.id),
                                ('res_model_id', '=', self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id),
                                ('user_id', '=', self.env.uid),
                                ('activity_type_id', '=', self.env.ref('inspire_approval.mail_act_activity').id)
                            ], limit=1)
        
                        if activity:
                            activity.action_feedback(feedback='Marked as done')
                        
                    
                else:
                    raise ValueError("The current user is not in the list of approvers.")
            else:
                raise ValueError("The purchase order does not have an associated approval request.")

    def refuse(self):
        for record in self:
            if record.approval_request_id:
                approval_request = record.approval_request_id
                current_user = self.env.user

                # Check if the current user is in the list of approvers of the approval category
                approvers = approval_request.category_id.approver_ids
                if current_user in approval_request.approver_ids.mapped('user_id'):
                
                    
                        approval_request.action_refuse()
                    
                else:
                    raise ValueError("The current user is not in the list of approvers.")
            else:
                raise ValueError("The purchase order does not have an associated approval request.")
    @api.model
    def notification_responsible(self, user_id, contract):
        activity_type = self.env.ref('inspire_approval.mail_notify_activity')
        summary = self._translate('Purchase Request')
        note = self._translate('There are a purchase request waiting for you')

        todos = {
            'res_id': contract.id,
            'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'purchase.order')]).id,
            'user_id': user_id,
            'summary': summary,
            'note': note,
            'activity_type_id': activity_type.id,
            'date_deadline': fields.Date.today(),
        }
        self.env['mail.activity'].with_user(user_id).create(todos)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for record in self:
            responsible_partner = record.order_type.responsible  # Fetch the responsible partner
            if responsible_partner:
                self.notification_responsible(responsible_partner.user_ids[0].id, record)  # Use the user ID of the responsible partner
        return res


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')


