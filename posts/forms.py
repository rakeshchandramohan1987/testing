from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, required
from flask_wysiwyg.wysiwyg import WysiwygField





class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    content = WysiwygField('Description', validators=[DataRequired()])
    tagname = StringField('Tags', validators=[DataRequired(), Length(min=5, max=100)])

    submit = SubmitField('Publish')


