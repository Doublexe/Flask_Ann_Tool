from flask import (render_template, url_for, flash, session,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
import yaml
from att import db
from att.models import Record
import os
import datetime
from att.annotation.utils import parse_dir, modify_record, store_meta, find_attribute
from att.static.root_path import Config


with open('./original.yaml', 'r') as f:
    original = yaml.load(f)


annotation = Blueprint('annotation', __name__)


@annotation.route("/render/<dir>/<record>", strict_slashes=False, methods=['GET'])
@login_required
def record(dir, record):

    if not current_user.id == Config.ADMIN_ID:
        q = Record.query.filter_by(dir=dir, record=record)
        if q.first() is not None:
            if q.first().user_id != current_user.id:
                return redirect(url_for("main.home"))
        else:
            db.session.begin_nested()
            try:
                db_record = Record(dir=dir, record=record, user_id=current_user.id)
                db.session.add(db_record)
                db.session.commit()
            except db.IntegrityError:
                db.session.rollback()
                return redirect(url_for("main.home"))

    report = Record.query.filter_by(dir=dir, record=record).first().report

    dir_path = os.path.join(Config.extracted_path, dir)

    records = [[r, False] for r in os.listdir(
        dir_path) if Config.record_pattern.search(r) is not None]  # need to be modified

    completed = False
    for record_thread in records:
        q = Record.query.filter_by(dir=dir, record=record_thread[0])
        if q.first() is not None:
            record_thread[1] = q.first().submit
            if record_thread[1] and record_thread[0]==record:
                completed = True

    next = None
    for record_thread in records:
        if record_thread[0] != record and not record_thread[1]:
            next = record_thread[0]

    record_path = os.path.join(dir_path, record)
    cameras, attributes = parse_dir(record_path)


    ori_cameras_ = original.get(dir, {}).get(record, {})
    ori_cameras = modify_record(ori_cameras_)
    # This force the ori_cameras, cameras, annotation to be the same format:
    #   dict{ Camera -> List[img] }


    # check temporary info
    meta_pth = session['meta_pth'] = os.path.join(record_path, 'meta.yaml')
    if not os.path.exists(meta_pth):
        meta = {
            'usr_finished': False,
            'admin_finished': False,
            'annotated': ori_cameras,
            'last_submit': str(datetime.datetime.now().date())
        }
        with open(meta_pth, 'w') as f:
            yaml.dump(meta, f)
    else:
        with open(meta_pth, 'r') as f:
            meta = yaml.full_load(f)

    annotated = meta['annotated']

    # The format of output: [tracklet/img_name, img(base64), annotated, original_annotated]
    output = {}
    for camera, tracklets in cameras.items():
        prior = []
        posterior = []
        for name, img_64 in tracklets:
            anno = True if name in annotated.get(camera,[]) else False
            orig = True if name in ori_cameras.get(camera,[]) else False
            out = (name, img_64, anno, orig)
            if anno or orig:
                prior.append(out)
            else:
                posterior.append(out)
        output[camera] = prior + posterior

    # for camera, tracklets in cameras.items():
    #     ls = []
    #     for name, img_64 in tracklets:
    #         anno = True if name in annotated.get(camera,[]) else False
    #         orig = True if name in ori_cameras.get(camera,[]) else False
    #         out = (name, img_64, anno, orig)
    #         ls.append(out)
    #     output[camera] = ls

    # store yaml into memory: 10 times JS action / submit -> yaml disk storage
    # render the annotations

    attributes = att = ''.join(
        c for c in attributes if c not in '(){}<>').split(r'_')
    attributes = [
        att[0].capitalize() + ' ' + att[2].capitalize(),
        att[1].capitalize() + ' ' + att[3].capitalize(),
        att[4].capitalize(),
        att[5].capitalize()
    ]
    return render_template('annotation.html', cameras=output, attributes=attributes, records=records, record=record, dir=dir, completed=completed, next=next, report=report)


@annotation.route("/submit", methods=['POST'])
@login_required
def submit():
    try:
        data = request.get_json()
        annotated = data['annotated']
        dir, record = data['dir'], data['record']
        report = data['report']
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
                'last_submit': str(datetime.datetime.now().date()),
                'report': report if report else None
            }
            with open(meta_pth, 'w') as f:
                yaml.dump(meta, f)

        if finished:
            record_db = Record.query.filter_by(dir=dir, record=record).first()
            record_db.submit = True
            record_db.report = report if report else None
            db.session.commit()
            store_meta(meta_pth)

    except ValueError:
        abort(500)
    return jsonify({'status': 'success'})
