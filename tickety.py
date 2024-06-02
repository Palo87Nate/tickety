#!/usr/bin/python3
""" Starts a Flash Web Application """
from models.storage import Session
from models.ticket import Ticket
from models.event import Event
from models.user import User
from forms import RegistrationForm, LoginForm, EventForm, TicketForm
from os import environ
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models.base_model import Session as DBSession
import io
import hashlib
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nate_palo_87'
CORS(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    DBSession.remove()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return DBSession.query(User).get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(name=form.name.data, password=hashed_password, email=form.email.data, pnumber=form.pnumber.data, logo=form.logo.data)
        DBSession.add(new_user)
        DBSession.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            Session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your information', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/create-event', methods=['GET', 'POST'], strict_slashes=False)
def create_event():
    form = EventForm(request.form)

    if form.validate_on_submit():
        ename = form.event_name.data
        date = form.date.data
        time = form.time.data
        venue = form.venue.data
        places = form.places.data
        details = form.details.data
        t_price = form.t_price.data
        
        event = Event(ename=ename, date=date, time=time, venue=venue, places=places, details=details, t_price=t_price)
            
        # Save to the database
        session = DBSession()
        try:
            session.add(event)
            session.commit()
            session.refresh(event)
            return render_template('our-events.html', event=event)
        
        except Exception as e:
            session.rollback()
            raise e
        
        finally:
            session.close()      
    return render_template('event.html', form=form, cache_id=uuid.uuid4())

@app.route('/buy-ticket', methods=['GET', 'POST'], strict_slashes=False)
def buy_ticket_route():
    form = TicketForm(request.form)

    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        pnumber = form.pnumber.data
        
        ticket = Ticket(fname=fname, lname=lname, email=email, pnumber=pnumber)
            
        # Save to the database
        session = DBSession()
        try:
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return render_template('confirm.html', ticket=ticket)
        
        except Exception as e:
            session.rollback()
            raise e
        
        finally:
            session.close()      
    return render_template('ticket.html', form=form, cache_id=uuid.uuid4())

@app.route('/qrcode/<ticket_id>')
def get_qrcode(ticket_id):
    # Retrieve the ticket from the database
    ticket = DBSession.query(Ticket).filter_by(id=ticket_id).first()
    if ticket:
        # Return the QR code image
        return send_file(io.BytesIO(ticket.qrcode), mimetype='image/png')
    else:
        return "", 404

@app.route('/browse-events')
def browse_events():
    if 'user_id' in Session:
        current_user_id = Session['user_id']
        events = DBSession.query(Event).filter(Event.user_id == current_user_id).all()
    else:
        events = DBSession.query(Event).all()
    return render_template('events.html', events=events)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
