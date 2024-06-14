#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField, EmailField, SubmitField, FileField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from .models.user import User

class RegistrationForm(FlaskForm):
    name = StringField('Company Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Business Email', validators=[InputRequired()])
    pnumber = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=15)])
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
    emage = FileField('Image')
    submit = SubmitField('Add Event')

class TicketForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('First Name', validators=[InputRequired()])
    email = EmailField('Business Email', validators=[InputRequired()])
    pnumber = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=15)])
    submit = SubmitField('Get Ticket')

class TiketSearchForm(FlaskForm):
    event_name = StringField('Event', validators=[InputRequired()])
    fname = StringField('Enter Your First Name', validators=[InputRequired()])
    lname = StringField('Enter Your Last Name', validators=[InputRequired()])
    submit = SubmitField('Get Ticket')

class ContactForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired()], render_kw={"placeholder": "email address"})
    message = TextAreaField('Message', validators=[InputRequired()], render_kw={"placeholder": "message"})
    submit = SubmitField('Send Message')

