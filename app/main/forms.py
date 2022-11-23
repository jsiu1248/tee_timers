from ast import Str
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField, SelectField, BooleanField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, NumberRange
from wtforms import widgets, SelectMultipleField
from app.models import db, Gender, Day, TimeOfDay, RideOrWalk, Handicap, Smoking, Drinking, PlayingType
from wtforms_sqlalchemy.fields import QuerySelectField

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
    description = TextAreaField("What's your response??") 
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
    # golf_course = SelectField('Golf Course', coerce=int, choices=[('')], validators=[])
    # city = SelectField('City', coerce=int, choices=[('')], validators=[])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender.choices = [(GenderDict.MALE, 'Male'),
                                     (GenderDict.FEMALE, 'Female'),
                                     (GenderDict.OTHER, 'Other')]
        self.day.choices = [(DayDict.MONDAY, 'Monday'),
                                     (DayDict.TUESDAY, 'Tuesday'),
                                     (DayDict.WEDNESDAY, 'Wednesday'), 
                                     (DayDict.THURSDAY, 'Thursday'), 
                                     (DayDict.FRIDAY, 'Friday'), 
                                     (DayDict.SATURDAY, 'Saturday'),
                                     (DayDict.SUNDAY, 'Sunday')]
        self.time_of_day.choices = [(TimeOfDayDict.MORNING, 'Morning'),
                                     (TimeOfDayDict.AFTERNOON, 'Afternoon')]
        self.ride_or_walk.choices = [(RideOrWalkDict.RIDE, 'Ride'), 
                             (RideOrWalkDict.WALK, 'Walk')]
        self.handicap.choices = [(HandicapDict.TWENTY, '20+'),
                                     (HandicapDict.FIFTEEN, '10-15'),
                                     (HandicapDict.TEN, '5-10'), 
                                     (HandicapDict.FIVE, '0-5')]
        self.smoking.choices = [(SmokingDict.NO, 'No'), (SmokingDict.YES, 'YES')]
        self.drinking.choices = [(DrinkingDict.NO, 'No'), (DrinkingDict.YES, 'YES')]
        self.playing_type.choices = [(PlayingTypeDict.LEISURE, 'Leisure'),
                                     (PlayingTypeDict.BETTING, 'Betting'),
                                     (PlayingTypeDict.COMPETITIVE, 'Competitive'), 
                                     (PlayingTypeDict.DRIVINGRANGE, 'Driving Range'),
                                     (PlayingTypeDict.LEARNING, 'Learning')]






class EditProfileForm(FlaskForm):
    """
    Entering or editting profile information.
    """
    # these two details have length validating limits
    name = StringField("Name", validators=[Length(0, 64)])
    age = IntegerField("Age", validators=[NumberRange(10, 120)])
    city = StringField("City", validators=[Length(0,64)])
    state = StringField("State", validators=[Length(0,64)])
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
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender.choices = [(GenderDict.MALE, 'Male'),
                                     (GenderDict.FEMALE, 'Female'),
                                     (GenderDict.OTHER, 'Other')]
        self.day.choices = [(DayDict.MONDAY, 'Monday'),
                                     (DayDict.TUESDAY, 'Tuesday'),
                                     (DayDict.WEDNESDAY, 'Wednesday'), 
                                     (DayDict.THURSDAY, 'Thursday'), 
                                     (DayDict.FRIDAY, 'Friday'), 
                                     (DayDict.SATURDAY, 'Saturday'),
                                     (DayDict.SUNDAY, 'Sunday')]
        self.time_of_day.choices = [(TimeOfDayDict.MORNING, 'Morning'),
                                     (TimeOfDayDict.AFTERNOON, 'Afternoon')]
        self.ride_or_walk.choices = [(RideOrWalkDict.RIDE, 'Ride'), 
                             (RideOrWalkDict.WALK, 'Walk')]
        self.handicap.choices = [(HandicapDict.TWENTY, '20+'),
                                     (HandicapDict.FIFTEEN, '10-15'),
                                     (HandicapDict.TEN, '5-10'), 
                                     (HandicapDict.FIVE, '0-5')]
        self.smoking.choices = [(SmokingDict.NO, 'No'), (SmokingDict.YES, 'YES')]
        self.drinking.choices = [(DrinkingDict.NO, 'No'), (DrinkingDict.YES, 'YES')]
        self.playing_type.choices = [(PlayingTypeDict.LEISURE, 'Leisure'),
                                     (PlayingTypeDict.BETTING, 'Betting'),
                                     (PlayingTypeDict.COMPETITIVE, 'Competitive'), 
                                     (PlayingTypeDict.DRIVINGRANGE, 'Driving Range'),
                                     (PlayingTypeDict.LEARNING, 'Learning')]


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
    city = StringField("City", validators=[Length(0,64)])
    state = StringField("State", validators=[Length(0,64)])
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

    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender.choices = [(GenderDict.MALE, 'Male'),
                                     (GenderDict.FEMALE, 'Female'),
                                     (GenderDict.OTHER, 'Other')]
        self.day.choices = [(DayDict.MONDAY, 'Monday'),
                                     (DayDict.TUESDAY, 'Tuesday'),
                                     (DayDict.WEDNESDAY, 'Wednesday'), 
                                     (DayDict.THURSDAY, 'Thursday'), 
                                     (DayDict.FRIDAY, 'Friday'), 
                                     (DayDict.SATURDAY, 'Saturday'),
                                     (DayDict.SUNDAY, 'Sunday')]
        self.time_of_day.choices = [(TimeOfDayDict.MORNING, 'Morning'),
                                     (TimeOfDayDict.AFTERNOON, 'Afternoon')]
        self.ride_or_walk.choices = [(RideOrWalkDict.RIDE, 'Ride'), 
                             (RideOrWalkDict.WALK, 'Walk')]
        self.handicap.choices = [(HandicapDict.TWENTY, '20+'),
                                     (HandicapDict.FIFTEEN, '10-15'),
                                     (HandicapDict.TEN, '5-10'), 
                                     (HandicapDict.FIVE, '0-5')]
        self.smoking.choices = [(SmokingDict.NO, 'No'), (SmokingDict.YES, 'YES')]
        self.drinking.choices = [(DrinkingDict.NO, 'No'), (DrinkingDict.YES, 'YES')]
        self.playing_type.choices = [(PlayingTypeDict.LEISURE, 'Leisure'),
                                     (PlayingTypeDict.BETTING, 'Betting'),
                                     (PlayingTypeDict.COMPETITIVE, 'Competitive'), 
                                     (PlayingTypeDict.DRIVINGRANGE, 'Driving Range'),
                                     (PlayingTypeDict.LEARNING, 'Learning')]
