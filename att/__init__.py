#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from att.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


"""
Logistics:
    1. Direcotries containing tracklets are basic subjects of operations. Meta information will be save in meta.yaml.
    2. The dir of all directories contain a dirs.txt with all finished dirnames.
    3. Valid ops: add/delete dirs, not modify finished ones.
    4. You can remark the finished ones to unfinished.
"""


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config())
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from att.main.routes import main
    from att.users.routes import users
    from att.annotation.routes import annotation
    from att.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(annotation)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app
