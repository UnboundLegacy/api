from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from career_connections.database import models

def configure_admin(app, db_session):
    '''Configure Admin pages for Career Connections'''
    admin = Admin(app, name='Unbound Legacy', template_mode='bootstrap3')
    admin.add_view(ModelView(models.User, db_session, name='Users'))
    admin.add_view(ModelView(models.PendingUser, db_session, name='Pending Users'))
