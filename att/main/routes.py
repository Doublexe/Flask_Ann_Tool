from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user
from att import bcrypt
from att.models import User
from att.users.forms import LoginForm

main = Blueprint('main', __name__)

@main.route("/", methods=['GET','POST'])
@main.route("/home", methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('annotation.render'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('annotation.render'))
        else:
            flash('Login Unsuccessful, Please check email and password','danger')
    return render_template('login.html', title='Login', form = form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
