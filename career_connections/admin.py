from flask import session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction

from career_connections.database import models

class BaseModelView(ModelView):

    def is_accessible(self):
        return session['is_authenticated']


class UserView(BaseModelView):
    can_create = False
    can_edit = False
    can_delete = False

    column_exclude_list = ['password']


class PendingUserView(BaseModelView):
    can_create = False
    can_edit = False

    column_extra_row_actions = [EndpointLinkRowAction('glyphicon glyphicon-ok', 'admin_views.approve_user')]

    def after_model_delete(self, model):
        print('Deleteing %s' % model.first_name)



def configure_admin(app, db_session):
    '''Configure Admin pages for Career Connections'''
    admin = Admin(app, name='Unbound Legacy', template_mode='bootstrap3')
    admin.add_view(UserView(models.User, db_session, name='Users'))
    admin.add_view(PendingUserView(models.PendingUser, db_session, name='Pending Users'))
