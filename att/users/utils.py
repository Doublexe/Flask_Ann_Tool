import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from att import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='linshanify@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token',token=token,_external=True)}

If you dod not make this request then simply ignore this email and no change made
'''
    mail.send(msg)
