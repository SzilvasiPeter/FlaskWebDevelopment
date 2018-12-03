import os
import secrets
from urllib.parse import urlparse, urlsplit
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt, mail
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm 
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form1 = LoginForm()
	if request.method == "POST":
		if form1.validate():
			user  = User.query.filter_by(email=form1.email.data).first()
			if user and bcrypt.check_password_hash(user.password, form1.password.data):
				flash('Login is successfull.', 'success')
				login_user(user, remember=form1.remember.data)
				# next_page = request.args.get('next')
				#return redirect(url_for('index') 
				#return redirect(next_page) if next_page else redirect(url_for('index')) # This broke the code somehow
			else:
				flash('Login Unsuccessfull. Your email or password is wrong', 'danger')
		else:
			flash('Invalid Inputs. Please fill valid email and password', 'warning')
		
	return render_template('mainPage.html', form1=form1)

@app.route('/blog/')
def blog():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
	return render_template('blog.html', posts=posts)

@app.route('/blog/about/')
def blog_about():
	return render_template('blogAbout.html', title='About')

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

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('blog'))
	form = LoginForm()
	if form.validate_on_submit():
		user  = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			flash('Login is successfull.', 'success')
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('blog'))
		else:
			flash('Login Unsuccessfull. Your email or password is wrong', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/logoutAtBlog')
def logoutAtBlog():
	logout_user()
	return redirect(url_for('blog'))

def save_picture(form_picture):
	#random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = f_name + '_resized' + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics/', picture_fn)
	
	output_size = (250, 250)
	i = Image.open(form_picture)
	width, height = i.size # 500x333
	# For other picture maybe resize
	cropped_image = i.crop((70, 0, width - 70, height))
	cropped_image.thumbnail(output_size)
	cropped_image.save(picture_path)

	return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if current_user.username == request.form['username'] and current_user.email == request.form['email'] and (request.form.get('picture') == '' or current_user.image_file == request.form.get('picture')):
			return redirect(url_for('account'))
		else:	
			if form.picture.data:
				picture_file = save_picture(form.picture.data)
				current_user.image_file = picture_file
			current_user.username = form.username.data
			current_user.email = form.email.data
			db.session.commit()
			flash('Your account has been updated', 'success')
			return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	else:
		flash('Edit was Unsuccessfull', 'danger')

	image_file = url_for('static', filename='profile_pics/' + current_user.image_file) 
	return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/pricing')
def pricing():
	return render_template('pricing.html', title='Pricing')

@app.route('/blogpost/new', methods=['GET', 'POST'])
@login_required
def new_blog_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been Created', 'success')
		return redirect(url_for('blog'))
	return render_template('create_blog_post.html', title='New Post', form=form, legend='New Post')

@app.route('/blogpost/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id) # We can use simple method: get() instead of get_or_404
	return render_template('post.html', title=post.title, post=post)

@app.route('/blogpost/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit() # Dont need to add, because they are already there
		flash('Your post has been updated', 'success')
		return redirect(url_for('post', post_id=post_id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_blog_post.html', title='Update Post', form=form, legend='Update Post')

@app.route('/blogpost/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted', 'success')
	return redirect(url_for('blog'))

@app.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query\
		.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=4)
	return render_template('user_posts.html', posts=posts, user=user)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
				sender='noreply@demo.com',
				recipients=[user.email])
	msg.body = f'''To reset your, password, visit the following ling:
{url_for('reset_token', token=token, _external=True) }

If you did not make this request then simply ignore this email and no changes will be made.
'''
	mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title='Reset Password', form=form) 

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pw
		db.session.commit()
		flash('Your password has been updated! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)