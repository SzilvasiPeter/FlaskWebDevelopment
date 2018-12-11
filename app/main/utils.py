from flask import url_for, flash, redirect, request
from flask_login import login_user
from app.users.forms import LoginForm
from app import db, bcrypt
from app.models import User

def indexLogin(form1):
	if request.method == "POST":
		if form1.validate():
			user = User.query.filter_by(email=form1.email.data).first()
			if user and bcrypt.check_password_hash(user.password, form1.password.data):
				flash('Login is successfull.', 'success')
				login_user(user, remember=form1.remember.data)
				next_page = request.args.get('next')
				#return redirect(url_for('index') 
				return redirect(next_page) if next_page else redirect(url_for('main.index'))
			else:
				flash('Login Unsuccessfull. Your email or password is wrong', 'danger')
		else:
			flash('Invalid Inputs. Please fill valid email and password', 'warning')