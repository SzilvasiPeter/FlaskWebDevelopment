from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		'author': 'Szilvasi Peter',
		'title': 'Blog Post1',
		'content': 'First post content',
		'date_posted': '2018.10.25'
	},
	{
		'author': 'John Doe',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date_posted': '2018.10.26'
	}
]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form1 = LoginForm()
	if request.method == "POST":
		if form1.validate():
			user  = User.query.filter_by(email=form1.email.data).first()
			if user and bcrypt.check_password_hash(user.password, form1.password.data):
				flash('Login is successfull.', 'success')
				login_user(user, remember=form1.remember.data)
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('index'))
			else:
				flash('Login Unsuccessfull. Your email or password is wrong', 'danger')
		else:
			flash('Invalid Inputs. Please fill valid email and password', 'warning')
		
	return render_template('mainPage.html', form1=form1)

@app.route('/dashboard/')
def dashboard():
	return render_template("dashboard.html")

@app.route('/blog/')
def blog():
	return render_template("blog.html", posts=posts, title="Blog")

@app.route('/blog/about/')
def blog_about():
	return render_template("blogAbout.html", title="About")

@app.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
	return render_template('account.html', title='Account')