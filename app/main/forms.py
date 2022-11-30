from ast import Str
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, SelectField, BooleanField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms import widgets, SelectMultipleField
from app.models import db, Gender
from app.models import City, GolfCourse, State, PlayingType, TimeOfDay, Smoking, Day, Drinking, RideOrWalk, Handicap
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed

class TechSupportForm(FlaskForm):
    """
    Form for asking any questions. 
    """
    title = StringField("Title")
    tech_message = TextAreaField("What would you like help with?") 
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    """
    Form for creating a post or reply. 
    """
    title = StringField("Title")
    description = TextAreaField("What are you up to?") 
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    """
    Form for creating a post or reply. 
    """
    description = TextAreaField("What's your response?") 
    submit = SubmitField("Submit")

class MatchForm(FlaskForm):
    """
    Form for user to select criteria of playing partner. 
    """
    gender = SelectMultipleField('Gender',
                               coerce=int,
                               validators=[])
    day = SelectMultipleField('Day',
                               coerce=int,
                               validators=[])
    time_of_day = SelectMultipleField('Time of Day',
                               coerce=int,
                               validators=[])

    ride_or_walk = SelectMultipleField('Ride or Walk',
                               coerce=int,
                               validators=[])
    handicap = SelectMultipleField('Handicap',
                               coerce=int,
                               validators=[])
    smoking = SelectMultipleField('Smoking',
                               coerce=int,
                               validators=[])
    drinking = SelectMultipleField('Drinking',
                               coerce=int,
                               validators=[])            
    playing_type = SelectMultipleField('Playing Type',
                               coerce=int,
                               validators=[])            
    golf_course = SelectField('Golf Course', coerce=int, choices=[('')], validators=[])
    city = SelectField('City', coerce=int, choices=[('')], validators=[])
    state = SelectField('State', coerce=int, choices=[('')], validators=[])

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender.choices = [(g.id, g.gender) for g in Gender.query.all()]
        self.day.choices = [(dy.id, dy.day) for dy in Day.query.all()]
        self.time_of_day.choices = [(td.id, td.time_of_day) for td in TimeOfDay.query.all()]
        self.ride_or_walk.choices = [(rw.id, rw.ride_or_walk) for rw in RideOrWalk.query.all()]
        self.handicap.choices = [(h.id, h.handicap) for h in Handicap.query.all()]
        self.smoking.choices = [(sm.id, sm.smoking) for sm in Smoking.query.all()]
        self.drinking.choices = [(d.id, d.drinking) for d in Drinking.query.all()]

        self.playing_type.choices = [(pt.id, pt.playing_type) for pt in PlayingType.query.all()]
        self.city.choices = [
            (c.id, c.city) for c in City.query.all()
        ]
        self.state.choices = [
            (s.id, s.state) for s in State.query.all()]

        self.golf_course.choices = [
            (g.id, g.course) for g in GolfCourse.query.all()]






class EditProfileForm(FlaskForm):
    """
    Entering or editting profile information.
    """
    # these two details have length validating limits
    name = StringField("Name", validators=[Length(0, 64)])
    age = IntegerField("Age", validators=[NumberRange(10, 120)])
    city = SelectField("City", validators=[])
    state = SelectField("State", validators=[])
    # users can write bios as long as they want
    bio = TextAreaField("Bio")
    gender = SelectMultipleField('Gender',
                               coerce=int,
                               validators=[])
    day = SelectMultipleField('Day',
                               coerce=int,
                               validators=[])
    time_of_day = SelectMultipleField('Time of Day',
                               coerce=int,
                               validators=[])

    ride_or_walk = SelectMultipleField('Ride or Walk',
                               coerce=int,
                               validators=[])
    handicap = SelectMultipleField('Handicap',
                               coerce=int,
                               validators=[])
    smoking = SelectMultipleField('Smoking',
                               coerce=int,
                               validators=[])
    drinking = SelectMultipleField('Drinking',
                               coerce=int,
                               validators=[])            
    playing_type = SelectMultipleField('Playing Type',
                               coerce=int,
                               validators=[])  
    golf_course = SelectField('Golf Course', coerce=int, choices=[('')], validators=[])
         
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender.choices = [(g.id, g.gender) for g in Gender.query.all()]
        self.day.choices = [(dy.id, dy.day) for dy in Day.query.all()]
        self.time_of_day.choices = [(td.id, td.time_of_day) for td in TimeOfDay.query.all()]
        self.ride_or_walk.choices = [(rw.id, rw.ride_or_walk) for rw in RideOrWalk.query.all()]
        self.handicap.choices = [(h.id, h.handicap) for h in Handicap.query.all()]
        self.smoking.choices = [(sm.id, sm.smoking) for sm in Smoking.query.all()]
        self.drinking.choices = [(d.id, d.drinking) for d in Drinking.query.all()]

        self.playing_type.choices = [(pt.id, pt.playing_type) for pt in PlayingType.query.all()]
        self.city.choices = [
            (c.id, c.city) for c in City.query.all()
        ]
        self.state.choices = [
            (s.id, s.state) for s in State.query.all()]

        self.golf_course.choices = [
            (g.id, g.course) for g in GolfCourse.query.all()]

        

class AdminLevelEditProfileForm(FlaskForm):
    # the admin can change the username
    username = StringField('Username', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames must have only letters, numbers, dots, or underscores',
        )])
    # the admin can change the confirmation
    confirmed = BooleanField("Confirmed")

    # field values are coerced into ints instead of str
    role = SelectField("Role", choices=[(1,"User"), (2, "Moderator"), (3, "Administrator")], coerce = int)
    name = StringField("Name", validators=[Length(0, 64)])
    age = IntegerField("Age", validators=[NumberRange(10, 120)])
    city = SelectField("City", validators = [])
    state = SelectField("State", validators=[])
    # users can write bios as long as they want
    bio = TextAreaField("Bio")
    gender = SelectMultipleField('Gender',
                               coerce=int,
                               validators=[])
    day = SelectMultipleField('Day',
                               coerce=int,
                               validators=[])
    time_of_day = SelectMultipleField('Time of Day',
                               coerce=int,
                               validators=[])

    ride_or_walk = SelectMultipleField('Ride or Walk',
                               coerce=int,
                               validators=[])
    handicap = SelectMultipleField('Handicap',
                               coerce=int,
                               validators=[])
    smoking = SelectMultipleField('Smoking',
                               coerce=int,
                               validators=[])
    drinking = SelectMultipleField('Drinking',
                               coerce=int,
                               validators=[])            
    playing_type = SelectMultipleField('Playing Type',
                               coerce=int,
                               validators=[])       
    golf_course = SelectField("Golf Course", choices=[('')],coerce=int, validators=[]) 
    picture =    FileField(label = "Update Profile Picture", validators=[FileAllowed('png', 'jpeg')]) 

    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender.choices = [(g.id, g.gender) for g in Gender.query.all()]
        self.day.choices = [(dy.id, dy.day) for dy in Day.query.all()]
        self.time_of_day.choices = [(td.id, td.time_of_day) for td in TimeOfDay.query.all()]
        self.ride_or_walk.choices = [(rw.id, rw.ride_or_walk) for rw in RideOrWalk.query.all()]
        self.handicap.choices = [(h.id, h.handicap) for h in Handicap.query.all()]
        self.smoking.choices = [(sm.id, sm.smoking) for sm in Smoking.query.all()]
        self.drinking.choices = [(d.id, d.drinking) for d in Drinking.query.all()]

        self.playing_type.choices = [(pt.id, pt.playing_type) for pt in PlayingType.query.all()]
        self.city.choices = [
            (c.id, c.city) for c in City.query.all()
        ]
        self.state.choices = [
            (s.id, s.state) for s in State.query.all()]

        self.golf_course.choices = [
            (g.id, g.course) for g in GolfCourse.query.all()]

        
