_author_ = 'Rakesh Chandramohan'

from datetime import datetime
from Glob import db, login_manager, create_app
from Glob.posts.utils import autoIncrement
from flask_login import UserMixin
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app



@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    datetime_str = datetime.now()
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(20), nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}', '{self.image_file}')"


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

entry_tags = db.Table('entry_tags',
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                      )

class Post(db.Model):
    datetime_str = datetime.now()
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Text, unique=False, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(250000), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Text, unique=False, nullable=False)
    slug = db.Column(db.String(100), unique=True)
    tags = db.Column(db.String(100))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args,**kwargs)
        # Call parent constructor.
        self.generate_slug()
    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)


    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag %s>' % self.name
