from flask import (render_template, url_for, flash, session,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
import yaml
from att import db
from att.models import DirLock, ClockLock, User
import os
import datetime
from att.annotation.utils import move_to_next, parse_dir, root
import re
from att.static.root_path import Config

annotation = Blueprint('annotation', __name__)


# def continue_dir(user_id, init=False):
#     ClockLock.acquire()
#     if not init:
#         cur_dir = DirLock.query.filter_by(user_id=current_user.id, finished=False).first()
#         cur_dir.finished = True
#         db.session.commit()
#
#     new_directory = move_to_next()
#
#     if new_directory is None:
#         ClockLock.release()
#         return None
#     else:
#         dirlock=DirLock(path=new_directory, user_id=user_id)
#         db.session.add(dirlock)
#         db.session.commit()
#         if init:
#             user = User.query.filter_by(id = current_user.id).first()
#             user.started = True
#             db.session.commit()
#         ClockLock.release()
#
#     return new_directory


record_name_pattern = re.compile(r'[\dA-Z]+_[A-Za-z\-]+_[A-Za-z]')


@annotation.route("/render/<dir>/<record>", strict_slashes=False, methods=['GET'])
@login_required
def record(dir, record):
    # dir_path = '/home/tangyingtian/dsta/WebAnnotationTesting/ExtractedImages/09-24-A/'
    # record = '5_shan_lin'
    extracted_path = Config.extracted_path
    dir_path = os.path.join(extracted_path, dir)

    records = [r for r in os.listdir(dir_path) if record_name_pattern.search(r) is not None]

    record_path = os.path.join(dir_path, record)

    cameras, attributes = parse_dir(record_path)  # return (name, base64, annotated)

    # check temporary info
    meta_pth = session['meta_pth'] = os.path.join(root, record_path, 'meta.yaml')
    if not os.path.exists(meta_pth):
        meta = {
            'usr_finished': False,
            'admin_finished': False,
            'annotated': {},
            'last_submit': str(datetime.datetime.now().date())
        }
        with open(meta_pth, 'w') as f:
            yaml.dump(meta, f)
    else:
        with open(meta_pth, 'r') as f:
            meta = yaml.full_load(f)

    annotated = meta['annotated']

    output = {}
    for camera, tracklets in cameras.items():
        if camera in annotated:
            output[camera] = [(name, img_64, True if name in annotated[camera] else False) for name, img_64 in tracklets]
        else:
            output[camera] = [(name, img_64, False) for name, img_64 in tracklets]
    # store yaml into memory: 10 times JS action / submit -> yaml disk storage
    # render the annotations

    attributes = att = ''.join(c for c in attributes if c not in '(){}<>').split(r'_')
    attributes = [
        att[0].capitalize()+' '+att[2].capitalize(),
        att[1].capitalize()+' '+att[3].capitalize(),
        att[4].capitalize(),
        att[5].capitalize()
    ]
    return render_template('annotation.html', cameras=output, attributes=attributes, records=records, record=record, dir=dir)



@annotation.route("/submit", methods=['POST'])
@login_required
def submit():
    try:
        data = request.get_json()
        annotated = data['annotated']
        annotation = {}
        for camera, tracklet in annotated:
            annotation.setdefault(camera, []).append(tracklet)
        finished = data['finished']
        meta_pth = session['meta_pth']
        if not os.path.exists(meta_pth):
            raise ValueError('meta path not initialized.')
        else:
            meta = {
                'usr_finished': finished,
                'admin_finished': False,
                'annotated': annotation,
                'last_submit': str(datetime.datetime.now().date())
            }
            with open(meta_pth, 'w') as f:
                yaml.dump(meta, f)

    except ValueError:
        abort(500)
    return jsonify({'status': 'success'})
