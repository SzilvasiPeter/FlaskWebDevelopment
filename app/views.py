from app import app
from flask import Flask, render_template, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm

app.config['SECRET_KEY'] = '63483d93977177f94771262462df57fb'

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

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	form1 = LoginForm()
	if form1.validate_on_submit():
		if form1.email.data == 'admin@gmail.com' and form1.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('index'))
		else:
			flash('Login Unsuccessfull. Please check username and password', 'danger')
			return redirect(url_for('index'))
	return render_template('mainPage.html', form=form1)
	# return render_template("mainPage.html")

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
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form=form)
