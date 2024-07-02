
'''
############################Grant APProve############################################
iif record.approval_request_id:
    approval_request = record.approval_request_id
    current_user = env.user

    # Check if the current user is in the list of approvers of the approval category
    approvers = approval_request.category_id.approver_ids
    if current_user in approval_request.approver_ids.mapped('user_id'):
    
        
            approval_request.action_approve()
        
    else:
        raise ValueError("The current user is not in the list of approvers.")
else:
    raise ValueError("The purchase order does not have an associated approval request.")




#######################Approval Request##################################


approval_request = env['approval.request'].create({
    'name': record.name,  # Use the name of the created purchase order
    'request_owner_id': env.user.id,
    'category_id': record.approval_scenario_2.id,  # Replace with your approval category ID
    'reason': 'This is an automated approval request.',
})
approval_request.write({'request_status': 'pending'})
# Update the purchase order with the created approval request ID
record.write({'approval_request_id': approval_request.id})
#Define the code to create approval request and notify approvers


# Send activities to notify the approvers
users= record.approval_request_id.approver_ids
user_ids=[]
contract=record
for user in users:
    user_id=user.user_id.id
    record.notification(user_id,contract) 

######################################refuse##################################
if record.approval_request_id:
    approval_request = record.approval_request_id
    current_user = env.user

    # Check if the current user is in the list of approvers of the approval category
    approvers = approval_request.category_id.approver_ids
    if current_user in approval_request.approver_ids.mapped('user_id'):
    
        
            approval_request.action_refuse()
        
    else:
        raise ValueError("The current user is not in the list of approvers.")
else:
    raise ValueError("The purchase order does not have an associated approval request.")






'''