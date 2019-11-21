from flask import (render_template, url_for, flash, session,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
import yaml
from att import db
from att.models import DirLock, ClockLock, User
import os
import datetime
from att.utils import move_to_next, parse_dir, root

annotation = Blueprint('annotation', __name__)


def continue_dir(user_id, init=False):
    ClockLock.acquire()
    if not init:
        cur_dir = DirLock.query.filter_by(user_id=current_user.id, finished=False).first()
        cur_dir.finished = True
        db.session.commit()

    new_directory = move_to_next()

    if new_directory is None:
        ClockLock.release()
        return None
    else:
        dirlock=DirLock(path=new_directory, user_id=user_id)
        db.session.add(dirlock)
        db.session.commit()
        if init:
            user = User.query.filter_by(id = current_user.id).first()
            user.started = True
            db.session.commit()
        ClockLock.release()

    return new_directory



@annotation.route("/render", methods=['GET','POST'])
@login_required
def render():
    user = User.query.filter_by(id = current_user.id).first()
    if not user.started:
        cur_dir=continue_dir(current_user.id, init=True)
        if cur_dir is None:
            return redirect(url_for('main.about'))
    else:
        # Once started, always have one unfinished (otherwise all finished)
        cur_dir_obj = DirLock.query.filter_by(user_id=current_user.id, finished=False).first()
        # if all finished, goto main.about
        if cur_dir_obj is None:
            return redirect(url_for('main.about'))
        else:
            cur_dir = cur_dir_obj.path

    tracklets = parse_dir(cur_dir)  # return (name, base64, annotated)

    while len(tracklets) == 0:
        cur_dir=continue_dir(current_user.id)
        if cur_dir is None:
            return redirect(url_for('main.about'))
        tracklets = parse_dir(cur_dir)

    # check temporary info
    meta_pth = session['meta_pth'] = os.path.join(root, cur_dir, 'meta.yaml')
    if not os.path.exists(meta_pth):
        meta = {
            'usr_finished': False,
            'admin_finished': False,
            'annotated': [],
            'last_submit': str(datetime.datetime.now().date())
        }
        with open(meta_pth, 'w') as f:
            yaml.dump(meta, f)
    else:
        with open(meta_pth, 'r') as f:
            meta = yaml.full_load(f)

    annotated = meta['annotated']

    tracklets = [(name, img_64, True if name in annotated else False) for name, img_64 in tracklets]
    # store yaml into memory: 10 times JS action / submit -> yaml disk storage

    # render the annotations
    return render_template('annotation.html', tracklets=tracklets)



@annotation.route("/submit", methods=['POST', 'GET'])
@login_required
def submit():
    try:
        data = request.get_json()
        annotated = data['annotated']
        finished = data['finished']
        meta_pth = session['meta_pth']
        if not os.path.exists(meta_pth):
            raise ValueError('meta path not initialized.')
        else:
            meta = {
                'usr_finished': finished,
                'admin_finished': False,
                'annotated': annotated,
                'last_submit': str(datetime.datetime.now().date())
            }
            with open(meta_pth, 'w') as f:
                yaml.dump(meta, f)

        if finished:
            cur_dir = continue_dir(current_user.id)
            if cur_dir is None:
                return jsonify({'status': 'finished'})
    except ValueError:
        abort(500)
    return jsonify({'status': 'sucess'})
