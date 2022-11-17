from ast import Str
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, SelectField, BooleanField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
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

class MatchForm(FlaskForm):
    gender = SelectMultipleField('Gender',
                               coerce=int,
                               choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')],
                               validators=[])
    day = SelectMultipleField('Day',
                               coerce=int,
                               choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), 
                               (6, 'Saturday'), (7,'Sunday')],
                               validators=[])
    time_of_day = SelectMultipleField('Time of Day',
                               coerce=int,
                               choices=[(1, 'Morning'), (2, 'Afternoon')],
                               validators=[])

    ride_or_walk = SelectMultipleField('Ride or Walk',
                               coerce=int,
                               choices=[(1, 'Ride'), (2, 'Walk')],
                               validators=[])
    handicap = SelectMultipleField('Handicap',
                               coerce=int,
                               choices=[(1, '20+'), (2, '15-20'), (3, '10-15'), (4, '5-10'), (5, '0-5')],
                               validators=[])
    smoking = SelectMultipleField('Smoking',
                               coerce=int,
                               choices=[(1, 'No'), (2, 'Yes')],
                               validators=[])
    drinking = SelectMultipleField('Drinking',
                               coerce=int,
                               choices=[(1, 'No'), (2, 'Yes')],
                               validators=[])            
    playing_type = SelectMultipleField('Playing Type',
                               coerce=int,
                               choices=[(1, 'Leisure'), (2, 'Betting'), (3, 'Competitive'), (4, 'Driving Range'), (5, 'Learning')],
                               validators=[])            
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    # these two details have length validating limits
    name = StringField("Name", validators=[Length(0, 64)])
    age = IntegerField("Age", validators=[NumberRange(10, 120)])
    city = StringField("City", validators=[Length(0,64)])
    state = StringField("State", validators=[Length(0,64)])
    # users can write bios as long as they want
    bio = TextAreaField("Bio")
    gender = SelectMultipleField('Gender',
                               coerce=int,
                               choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')],
                               validators=[])
    day = SelectMultipleField('Day',
                               coerce=int,
                               choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), 
                               (6, 'Saturday'), (7,'Sunday')],
                               validators=[])
    time_of_day = SelectMultipleField('Time of Day',
                               coerce=int,
                               choices=[(1, 'Morning'), (2, 'Afternoon')],
                               validators=[])

    ride_or_walk = SelectMultipleField('Ride or Walk',
                               coerce=int,
                               choices=[(1, 'Ride'), (2, 'Walk')],
                               validators=[])
    handicap = SelectMultipleField('Handicap',
                               coerce=int,
                               choices=[(1, '20+'), (2, '15-20'), (3, '10-15'), (4, '5-10'), (5, '0-5')],
                               validators=[])
    smoking = SelectMultipleField('Smoking',
                               coerce=int,
                               choices=[(1, 'No'), (2, 'Yes')],
                               validators=[])
    drinking = SelectMultipleField('Drinking',
                               coerce=int,
                               choices=[(1, 'No'), (2, 'Yes')],
                               validators=[])            
    playing_type = SelectMultipleField('Playing Type',
                               coerce=int,
                               choices=[(1, 'Leisure'), (2, 'Betting'), (3, 'Competitive'), (4, 'Driving Range'), (5, 'Learning')],
                               validators=[])           
    submit = SubmitField("Submit")
