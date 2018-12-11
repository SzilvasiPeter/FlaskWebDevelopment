from flask import render_template,url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.users.forms import LoginForm
from app import db, bcrypt
from app.models import Post, User
from app.main.utils import indexLogin

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
	#if current_user.is_authenticated:
	#	return redirect(url_for('index')) # This broke the code somehow
	form1 = LoginForm()
	indexLogin(form1)
	return render_template('main/mainPage.html', form1=form1)

@main.route('/features/', methods=['GET', 'POST'])
def features():
	form1 = LoginForm()
	indexLogin(form1)
	return render_template('main/features.html', title='Features', form1=form1)

@main.route('/pricing')
@login_required
def pricing():
	return render_template('main/pricing.html', title='Pricing')

@main.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))
