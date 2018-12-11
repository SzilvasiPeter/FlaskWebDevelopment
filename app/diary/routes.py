from flask import render_template,url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app.users.forms import LoginForm
from app import db, bcrypt
from app.models import Post, User
from app.main.utils import indexLogin

diary = Blueprint('diary', __name__)

@diary.route('/diet/', methods=['GET', 'POST'])
@login_required
def diet():
	form1 = LoginForm()
	indexLogin(form1)
	return render_template('main/diary.html', title='Diary', form1=form1)