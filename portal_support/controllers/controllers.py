# from odoo import http
# from odoo.http import request

# class TaskPortal(http.Controller):

#     @http.route('/create/task', type='http', auth='user', website=True)
#     def create_task_form(self, project_id=None, **kw):
#         users = request.env['res.users'].sudo().search([])
#         return request.render('portal_support.create_task_form', {
#             'users': users,
#             'project_id': int(project_id) if project_id else None
#         })

#     @http.route('/create/task/submit', type='http', auth='user', methods=['POST'], website=True, csrf=False)
#     def submit_task(self, **post):
#         project_id = int(post.get('project_id')) if post.get('project_id') else None
#         task_name = post.get('task_name')
#         description = post.get('description')
#         #user_id = int(post.get('user_id'))
#         deadline = post.get('deadline')

#         task_values = {
#             'name': task_name,
#             'description': description,
#             #'user_ids': [(6, 0, [user_id])],  # Use a many2many relation properly
#             'date_deadline': deadline,
#         }

#         if project_id:
#             task_values['project_id'] = project_id

#         request.env['project.task'].sudo().create(task_values)
#         return request.redirect('/my/tasks')
# controllers/task_portal.py
# controllers/task_portal.py
from odoo import http
from odoo.http import request
from odoo.addons.project.controllers.portal import ProjectCustomerPortal as PortalCustomerView

class TaskPortal(PortalCustomerView):

    @http.route('/create/task', type='http', auth='user', website=True)
    def create_task_form(self, project_id=None, **kw):
        user = request.env.user
        allowed_projects = self._get_allowed_projects(user)
        users = request.env['res.users'].sudo().search([])
        return request.render('portal_support.create_task_form', {
            'users': users,
            'project_id': int(project_id) if project_id else None,
            'allowed_projects': allowed_projects
        })

    @http.route('/create/task/submit', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def submit_task(self, **post):
        project_id = post.get('project_id')
        task_name = post.get('task_name')
        description = post.get('description')
        deadline = post.get('deadline')

        # Try to find the project by ID first, if not, then by name
        project = request.env['project.project'].sudo().search(
            [('id', '=', int(project_id))] if project_id.isdigit() else [('name', '=', project_id)], limit=1
        )

        if not project:
            return request.redirect('/create/task?error=project_not_found')

        task_values = {
            'name': task_name,
            'description': description,
            'date_deadline': deadline,
            'project_id': project.id,
        }

        request.env['project.task'].sudo().create(task_values)
        return request.redirect('/my/tasks')

    def _get_allowed_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Project = request.env['project.project']
        domain = self._prepare_project_domain()

        searchbar_sortings = self._prepare_searchbar_sortings()
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # Fetch projects based on the domain and orders
        project_ids = Project.search(domain).mapped('id')

        # Apply additional filtering criteria
        allowed_projects = Project.sudo().search([
            ('id', 'in', project_ids),
            ('sale_order_id.order_line.product_id.name', '=', 'Support contract')
        ], order=order)

        return allowed_projects
# from odoo import http
# from odoo.http import request

# class ProjectPortal(http.Controller):

#     @http.route('/my/tasks', type='http', auth='user', website=True)
#     def portal_tasks_list(self, **kw):
#         projects = request.env['project.project'].sudo().search([])
#         tasks = request.env['project.task'].sudo().search([('user_id', '=', request.env.user.id)])
#         return request.render('project.portal_tasks_list', {
#             'projects': projects,
#             'tasks': tasks
#         })
