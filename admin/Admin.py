from flask_admin import Admin
from flask_admin.menu import MenuLink

from admin.Views import HomeView, UserView, GenericView
from model import *


def start_views(app, db):
    admin = Admin(app, name='Dashboard', base_template='admin/base.html', template_mode='bootstrap3',
                  index_view=HomeView())

    admin.add_view(GenericView(Role, db.session, 'Funções', category='Usuários'))
    admin.add_view(UserView(User, db.session, 'Usuários', category='Usuários'))
    admin.add_view(GenericView(State, db.session, 'Estados'))
    admin.add_view(GenericView(Disease, db.session, 'Doenças', category='Hospital'))
    admin.add_view(GenericView(Patient, db.session, 'Pacientes', category='Hospital'))
    admin.add_view(GenericView(DiseaseState, db.session, 'Estado dos Pacientes', category='Hospital'))

    admin.add_link(MenuLink(name='Logout', url='/logout'))
