from calendar import Calendar
from datetime import date
from flask import Flask, render_template,url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app.users.forms import LoginForm
from app import db
from app.models import User
from app.main.utils import indexLogin

diary = Blueprint('diary', __name__)

@diary.route('/diet/', methods=['GET', 'POST'])
@login_required
def diet():
	form1 = LoginForm()
	indexLogin(form1)
	return render_template('main/diary.html', title='Diary', form1=form1)

@diary.route('/', defaults={'year': None})
@diary.route('/<int:year>/')
def index(year):
    cal = Calendar(0)
    try:
        if not year:
            year = date.today().year
        cal_list = [
            cal.monthdatescalendar(year, i+1)
            for i in range(12)
        ]
    except:
        abort(404)
    else:
        return render_template('cal.html', year=year, cal=cal_list)
    abort(404)