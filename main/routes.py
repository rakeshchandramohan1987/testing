_author_ = 'Rakesh Chandramohan'

from flask import render_template, request, Blueprint
from Glob.models import Post

from sqlalchemy import cast, func, asc, desc
#import flask_whooshalchemy as wa

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    # results = Post.query.order_by().desc()
    posts = Post.query.order_by(desc(Post.date_posted))
    tagdict = {}
    for post in posts:
        strtags = str(post.tags)
        if strtags == "None":
            strtags = ""
        tagdict[post.id] = strtags.split(',')

    return render_template('home.html', posts=posts, tagdict=tagdict)


@main.route("/about")
def about():
    return render_template('about.html', title='About')