from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,Response)
from att import db, admin, basic_auth
from att.models import User, Record
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException

admin_pannel = Blueprint('admin_pannel', __name__)

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class ModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

admin.add_view(ModelView(Record, db.session, menu_icon_type='glyph', menu_icon_value='glyphicon-user'))

class ModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

admin.add_view(ModelView(User, db.session, menu_icon_type='glyph', menu_icon_value='glyphicon-user'))

class ReturnView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('main.home'))

admin.add_view(ReturnView(name='Return', menu_icon_type='glyph', menu_icon_value='glyphicon-home'))
