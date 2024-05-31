#!/usr/bin/python3
""" Starts a Flash Web Application """
from models.storage import create_ticket as create_ticket_in_storage, get_your_ticket, Session
from models.ticket import Ticket
from models.event import Event
from forms import EventForm, TicketForm
from os import environ
from flask import Flask, render_template, request, redirect, url_for
import uuid
from models.base_model import Session as DBSession

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

#help?

@app.teardown_appcontext
def shutdown_session(exception=None):
    DBSession.remove()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_ticket_view', methods=['GET', 'POST'], strict_slashes=False)
def create_ticket_view():
    event_form = EventForm(request.form)
    ticket_form = TicketForm(request.form)

    if event_form.validate_on_submit() and ticket_form.validate_on_submit():
        event_name = event_form.event_name.data
        date = event_form.date.data
        time = event_form.time.data
        venue = event_form.venue.data
        price = ticket_form.price.data
        
        # Create the event and ticket
        event = Event(name=event_name, date=date, time=time, venue=venue)
        ticket = Ticket(event_name=event_name, price=price)
            
        # Save to the database
        session = DBSession()
        try:
            session.add(event)
            session.add(ticket)
            session.commit()
            
            # Refresh both event and ticket objects to ensure they are fully populated
            session.refresh(event)
            session.refresh(ticket)
            
            return render_template('ticket.html', event=event, ticket=ticket)
        
        except Exception as e:
            session.rollback()
            raise e
        
        finally:
            session.close()      
    return render_template('tickety.html', event_form=event_form, ticket_form=ticket_form, cache_id=uuid.uuid4())    

@app.route('/ticket', methods=['GET', 'POST'], strict_slashes=False)
def ticket():
    tickets = DBSession.query(Ticket).all()
    return render_template('ticket.html', tickets=tickets)

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
