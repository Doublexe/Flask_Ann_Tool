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

    # if not current_user.is_authenticated:
        # form = LoginForm()
        # if form.validate_on_submit():
        #     user = User.query.filter_by(email=form.email.data).first()
        #     if user and bcrypt.check_password_hash(user.password,form.password.data):
        #         login_user(user,remember=form.remember.data)
        #         return render_template('home.html',date_list=date_list,date_dict=date_dict,dir_dict=dir_dict)
        #     else:
        #         flash('Login Unsuccessful, Please check email and password','danger')
        # return render_template('login.html', title='Login', form = form)
        # redirect('user.login')


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
        if started !=0:
            user_id = Record.query.filter_by(dir=dir).first().user_id
            user = User.query.filter_by(id=user_id).first().username
        else:
            user = None
            user_id = None

        date_dict.setdefault(date, []).append((dir, total, submits, user, user_id))

        record_list = []
        records = os.listdir(os.path.join(extracted_path,dir))
        for record in records:
            if os.path.isdir(os.path.join(extracted_path,dir,record)):
                record_list.append(record)
        record_list.sort()
        dir_dict[dir]=record_list
    date_list.sort()


    def is_finished(date):
        if not hasattr(current_user, 'id'):
            all_finished = True
            for _, total, submits, _, _ in date_dict[date]:
                if total != submits:
                    all_finished = False
            return False, False, all_finished
        selected = False
        finished = True
        all_finished = True
        for _, total, submits, user, user_id in date_dict[date]:
            if user_id == current_user.id:
                selected = True
            if total != submits:
                all_finished = False
                if user_id == current_user.id:
                    finished = False
        return selected, finished and selected, all_finished

    date_list = [(date, *is_finished(date)) for date in date_list]


    return render_template('home.html', date_list = date_list,date_dict=date_dict,dir_dict=dir_dict)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
