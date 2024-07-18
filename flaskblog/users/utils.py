import secrets, os
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail #, app
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics/',
                                 picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com',
                   recipients=[user.email])
    msg.body = f'''To Reset you password click on the following link:
{url_for('users.reset_token', token = token, _external = True)}

If you do not make this request, this simply ignore this email and no changes will be made.
'''
    mail.send(msg)