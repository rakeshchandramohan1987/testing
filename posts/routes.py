_author_ = 'Rakesh Chandramohan'

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from Glob import db
from Glob.models import Post
from Glob.posts.forms import PostForm
from uuid import uuid5


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=request.form.get('content'), author=current_user, status='Pending', tags=form.tagname.data)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created! It is been reviewed by our team and will be published as soon as possible. ', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route("/post/<string:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<string:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = request.form['content']
        post.tags = form.tagname.data
        db.session.commit()
        flash('Your Post has been updated successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        #request.content.data = post.content
        print(dir(request.form.values))
        form.tagname.data = post.tags
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')



@posts.route("/post/<string:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.status = 'Deactivate'
    db.session.commit()
    flash('Your Post has been deleted successfully!', 'success')
    return redirect(url_for('main.home'))