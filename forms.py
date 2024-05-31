#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField
from wtforms.validators import InputRequired

#help?

class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    venue = StringField('Venue', validators=[InputRequired()])

class TicketForm(FlaskForm):
    event_name = StringField('Event Name', validators=[InputRequired()])
    price = IntegerField('Ticket Price', validators=[InputRequired()])

