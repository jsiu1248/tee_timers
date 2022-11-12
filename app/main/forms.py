from ast import Str
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


class TechSupportForm(FlaskForm):
    title = StringField("Title")
    tech_message = TextAreaField("What would you like help with?") 
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    title = StringField("Title")
    comment_message = TextAreaField("What are you up to?") 
    submit = SubmitField("Submit")
