from app import app
from flask import Flask, render_template, url_for
# from app.forms import RegistrartionForm, LoginForm

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
@app.route('/index')
def index():
	return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
	return render_template("dashboard.html")

@app.route('/blog/')
def blog():
	return render_template("blog.html", posts=posts, title="Blog")

@app.route('/blog/about/')
def blog_about():
	return render_template("blogAbout.html", title="About")

# @app.route('/register/')
# def register():
# 	form = RegistrartionForm()
# 	return render_template('register.html', title='Register', form=form)

# @app.route('/login/')
# def login():
# 	form = LoginForm()
# 	return render_template('login.html', title='Login', form=form)