from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.posts.forms import PostForm


posts = Blueprint('posts', __name__)

@posts.route('/blog/')
def blog():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
	return render_template('blog/blog.html', posts=posts)

@posts.route('/blogpost/new', methods=['GET', 'POST'])
@login_required
def new_blog_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been Created', 'success')
		return redirect(url_for('posts.blog'))
	return render_template('blog/create_blog_post.html', title='New Post', form=form, legend='New Post')

@posts.route('/blogpost/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id) # We can use simple method: get() instead of get_or_404
	return render_template('blog/post.html', title=post.title, post=post)

@posts.route('/blogpost/<int:post_id>/update', methods=['GET', 'POST'])
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
		return redirect(url_for('posts.post', post_id=post_id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('blog/create_blog_post.html', title='Update Post', form=form, legend='Update Post')

@posts.route('/blogpost/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted', 'success')
	return redirect(url_for('posts.blog'))