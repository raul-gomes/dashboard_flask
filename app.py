import json, datetime

from flask_login import login_user, logout_user, LoginManager

import controllers as ctrl

from flask import Flask, request, Response, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from admin.Admin import start_views
from flask_bootstrap import Bootstrap

from forms import LoginForm


def create_app(config):
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.secret_key = config.SECRET
    app.config.from_object(config)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['FLASK_ADMIN_SWATCH'] = 'paper'  # Admin
    db = SQLAlchemy(app)  # Database

    start_views(app, db)  # Admin
    Bootstrap(app)  # Admin

    db.init_app(app)  # Database
    config.APP = app

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content_Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    @app.route('/report', methods=['POST'])
    def report():
        state = request.form['state']
        disease = request.form['disease']
        patients = ctrl.reportBystate(state, disease)

        return Response(json.dumps(patients, ensure_ascii=False), mimetype='application/json'), 200, {}

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm(request.form)
        if request.method == 'GET':
            data = {'status': 200, 'msg': None, 'type': None, 'form': form}
        else:
            if form.validate():
                user = ctrl.login(form.email.data, form.password.data)
                if user:
                    login_user(user, remember=True, duration=datetime.timedelta(minutes=5), fresh=True)
                    return redirect('/admin')
                else:
                    data = {'status': 401, 'msg': 'Dados de usuários incorretos', 'type': 1, 'form': form}
            else:
                data = {'status': 401, 'msg': 'Formulário inválido', 'type': 1, 'form': form}
        return render_template('login.html', data=data)

    @app.route('/logout')
    def logout_send():
        logout_user()
        form = LoginForm()
        return render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type': 3, 'form': form})

    @login_manager.user_loader
    def load_user(user_id):
        return ctrl.getUserById(user_id)
