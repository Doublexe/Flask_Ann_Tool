from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user
from att import bcrypt
from att.models import User, Record
from att.users.forms import LoginForm
from att.static.root_path import Config
import os

main = Blueprint('main', __name__)

@main.route("/", methods=['GET','POST'])
@main.route("/home", methods=['GET','POST'])
def home():
    extracted_path = Config.extracted_path

    dir_list = []
    files = os.listdir(extracted_path)
    for dir in files:
        if os.path.isdir(os.path.join(extracted_path,dir)):
            dir_list.append(dir)
    dir_list.sort()

    date_list = []
    date_dict = {}
    dir_dict = {}
    for dir in dir_list:
        month,day,_ = dir.split('-')
        date = month+"-"+day
        if date not in date_list:
            date_list.append(date)

        total = len([r for r in os.listdir(os.path.join(Config.extracted_path, dir)) if Config.record_pattern.search(r) is not None])
        started = Record.query.filter_by(dir=dir).count()
        submits = Record.query.filter_by(dir=dir, submit=True).count()
        user = None
        if started !=0:
            user_id = Record.query.filter_by(dir=dir).first().user_id
            user = User.query.filter_by(id=user_id).first().username

        date_dict.setdefault(date, []).append((dir, total, submits, user))

        record_list = []
        records = os.listdir(os.path.join(extracted_path,dir))
        for record in records:
            if os.path.isdir(os.path.join(extracted_path,dir,record)):
                record_list.append(record)
        record_list.sort()
        dir_dict[dir]=record_list
    date_list.sort()

    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                return render_template('home.html',date_list=date_list,date_dict=date_dict,dir_dict=dir_dict)
            else:
                flash('Login Unsuccessful, Please check email and password','danger')
        return render_template('login.html', title='Login', form = form)

    return render_template('home.html', date_list = date_list,date_dict=date_dict,dir_dict=dir_dict)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
