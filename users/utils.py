import os
import secrets
from PIL import Image
from flask import url_for, current_app, render_template, request
from Glob import mail
from flask_mail import Message
from sightengine.client import SightengineClient
from nude import Nude



def check_image(pic):
    pic = os.path.join(current_app.root_path, 'static/profile_pics', pic)
    picsamp = pic.replace('\\', '/')
    client = SightengineClient('82714170', 'RT4oo9fZFDbNsrvV6VSp')

    output = client.check('nudity', 'wad', 'celebrities', 'scam', 'face-attributes').set_file(picsamp)
    invalidImage = False
    # contains nudity
    if output['nudity']['safe'] <= output['nudity']['partial'] and output['nudity']['safe'] <= output['nudity']['raw']:
        invalidImage = True

    n = Nude(picsamp)
    n.parse()


    print(n.result, n.message)


    return invalidImage

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='rakesh.chandramohan@gmail.com',
                  recipients=[user.email])
    sbodycontent = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''


    # msg.body = sbodycontent + render_template('footer.html')
    msg.html = sbodycontent + render_template('footer.html')
    mail.send(msg)