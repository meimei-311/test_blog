#encoding: utf-8

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from ..auth.forms import Province_choice
# from pymongo import MongoClient
from wtforms import ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_pagedown.fields import PageDownField





class PostForm(Form):
    body = PageDownField('有什么想说的吗？', validators=[Required()])
    submit = SubmitField('发表')


class EditPostForm(Form):
    body = PageDownField('', validators=[Required()])
    submit = SubmitField('修改')


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('发布')
