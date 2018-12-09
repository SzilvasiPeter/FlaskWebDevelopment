import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail

def save_picture(form_picture):
	#random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = f_name + '_resized' + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics/', picture_fn)
	
	output_size = (250, 250)
	i = Image.open(form_picture)
	width, height = i.size # 500x333
	# For other picture maybe resize
	cropped_image = i.crop((70, 0, width - 70, height))
	cropped_image.thumbnail(output_size)
	cropped_image.save(picture_path)

	return picture_fn

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
				sender='noreply@demo.com',
				recipients=[user.email])
	msg.body = f'''To reset your, password, visit the following ling:
{url_for('users.reset_token', token=token, _external=True) }

If you did not make this request then simply ignore this email and no changes will be made.
'''
	mail.send(msg)