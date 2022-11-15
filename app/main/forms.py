from ast import Str
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import widgets, SelectMultipleField


class TechSupportForm(FlaskForm):
    title = StringField("Title")
    tech_message = TextAreaField("What would you like help with?") 
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    title = StringField("Title")
    comment_message = TextAreaField("What are you up to?") 
    submit = SubmitField("Submit")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    string_of_files = ['one\r\ntwo\r\nthree\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)

class ExampleForm(FlaskForm):
    nums = MultiCheckboxField('label',
                               coerce=int,
                               choices=[(1, 'one'), (2, 'two'), (3, 'three')],
                               validators=[])
    gender = MultiCheckboxField('gender',
                               coerce=int,
                               choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')],
                               validators=[])
    submit = SubmitField('submit')