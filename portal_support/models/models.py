# # from odoo import models, fields,api

# # class ProjectProject(models.Model):
# #     _inherit = 'project.project'

# #     has_support_contract = fields.Boolean(compute='_compute_has_support_contract', store=True)
# #     @api.model
# #     def _compute_has_support_contract(self):
# #         for project in self:
# #             print(project.id)
# #             # Assuming there is a 
# #             if project.allow_timesheets:
# #                 print("yes")
# #                 print(project.sale_line_id)
# #                 has_support_contract=True
# #             else: print("no")
# #             # # many2many or one2many relation to sale.order on the project
# #             # support_contract = any(
# #             #     line.product_id.name == 'Support Contract'
# #             #     for so in project.sale_line_id
# #             #     for line in so.order_line
# #             # )
# #             # project.has_support_contract = support_contract
# from odoo import models, fields, api

# class ProjectProject(models.Model):
#     _inherit = 'project.project'

#     support_contract = fields.Boolean(compute='_compute_support_contract', store=True)

#     @api.model
#     def _compute_support_contract(self):
#         for project in self:
#             print("Support")  # This line prints "Support" for each project
            
#             try:
#                 print("Support contract")  # This line prints "Support contract"
                
#                 # Check if project.allow_billable is True
#                 if project.allow_billable:
#                     # Check if project.sale_line_id and project.sale_line_id.project_id exist
#                     if project.sale_line_id and project.sale_line_id.project_id == "Support contract":
#                         project.support_contract = True
#                     else:
#                         project.support_contract = False
#                 else:
#                     project.support_contract = False
#             except:
#                 # If any exception occurs during the try block, set project.support_contract to False
#                 project.support_contract = False

#     @api.model
#     # def create(self, vals):
#     #     project = super(ProjectProject, self).create(vals)
#     #     project._compute_support_contract()
#     #     return project

#     # def write(self, vals):
#     #     res = super(ProjectProject, self).write(vals)
#     #     self._compute_support_contract()
#     #     return res

#     def read(self, fields=None, load='_classic_read'):
#         result = super(ProjectProject, self).read(fields, load)
#         self._compute_support_contract()
#         return result
