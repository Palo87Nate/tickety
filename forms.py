#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField, EmailField, SubmitField, FileField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models.user import User

class RegistrationForm(FlaskForm):
    name = StringField('Company Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Business Email', validators=[InputRequired()])
    pnumber = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=15)])
    logo = FileField('Your Logo (PNG Format)')
    submit = SubmitField('Register')
    
    def validate_username(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('A company with that name is already registered.')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    ename = StringField('Event Name', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    venue = StringField('Venue', validators=[InputRequired()])
    places = IntegerField('Number of places', validators=[InputRequired()])
    details = TextAreaField('Describe your event', validators=[InputRequired()])
    t_price = IntegerField('Ticket Price', validators=[InputRequired()])
    submit = SubmitField('Add Event')

class TicketForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('First Name', validators=[InputRequired()])
    email = EmailField('Business Email', validators=[InputRequired()])
    pnumber = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=15)])
    submit = SubmitField('Get Ticket')

