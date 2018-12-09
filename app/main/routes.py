from flask import render_template,url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.users.forms import LoginForm
from app import db, bcrypt
from app.models import Post, User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
	#if current_user.is_authenticated:
	#	return redirect(url_for('index')) # This broke the code somehow
	form1 = LoginForm()
	indexLogin(form1)
	return render_template('mainPage.html', form1=form1)

@main.route('/about/')
def about():
	form1 = LoginForm()
	indexLogin(form1)
	return render_template('about.html', title='About', form1=form1)

@main.route('/features/')
def features():
	form1 = LoginForm()
	indexLogin(form1)
	return render_template('features.html', title='Features', form1=form1)

@main.route('/pricing')
def pricing():
	return render_template('pricing.html', title='Pricing')

@main.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

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
