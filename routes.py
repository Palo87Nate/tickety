#!/usr/bin/python3
from flask import render_template, redirect, url_for, flash, send_file, request, Blueprint, current_app
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Event, Ticket, Session as session, storage
from .models.storage import create_event
from .forms import *
from sqlalchemy.orm.exc import NoResultFound
from math import ceil
from datetime import datetime
from flask_mail import Mail, Message
from .files import generate_pdf_ticket
import uuid, io, os

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    events = session.query(Event).all()
    return render_template('index.html', events=events)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            pnumber=form.pnumber.data
        )
        new_user.set_password(form.password.data)
        
        new_user.save(session)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('routes.index'))
        ''' except Exception as e:
            flash('An error occurred. Please try again later.', 'danger') '''
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            flash('Login Unsuccessful. Please check your information', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/create-event', methods=['GET', 'POST'], strict_slashes=False)
def create_event_view():
    form = EventForm(request.form)
    if form.validate_on_submit():
        file = request.files['emage']
        if file and file.filename != '':
            image_data = file.read()
        try:
            create_event(
                ename=form.ename.data,
                date=form.date.data,
                time=form.time.data,
                venue=form.venue.data,
                places=form.places.data,
                details=form.details.data,
                t_price=form.t_price.data,
                emage=image_data,
                user_id=current_user.id
            )
            flash('Event created successfully!', 'success')
            return redirect(url_for('routes.browse_events'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
    
    return render_template('create-event.html', form=form, cache_id=uuid.uuid4())

@bp.route('/event/<event_id>')
def event_details(event_id):
    event = session.query(Event).get(event_id)
    if event:
        sold_tickets = session.query(Ticket).filter_by(event_id=event_id).count()
        remaining_tickets = event.places - sold_tickets
        formatted_date = event.date.strftime('%d-%b')
        formatted_time = event.time.strftime('%H:%M')
        return render_template('event.html', event=event, formatted_date=formatted_date, remaining_tickets=remaining_tickets, formatted_time=formatted_time)
    else:
        return render_template('event_not_found.html'), 404


@bp.route('/buy-ticket/<event_id>', methods=['GET', 'POST'], strict_slashes=False)
def buy_ticket(event_id):
    form = TicketForm(request.form)
    event = session.query(Event).get(event_id)
    if event and form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        pnumber = form.pnumber.data
        event_id = event_id
        ticket = Ticket(fname=fname, lname=lname, email=email, pnumber=pnumber, event_id=event_id)
            
        try:
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            ticket_id = ticket.id
            return redirect(url_for('routes.confirm_ticket', event_id=event_id, ticket_id=ticket_id))
        
        except Exception as e:
            session.rollback()
            raise e
        
        finally:
            session.close()      
    return render_template('ticket.html', form=form, event=event, cache_id=uuid.uuid4())

@bp.route('/confirm-ticket/<event_id>/<ticket_id>')
def confirm_ticket(event_id, ticket_id):
    print("Request args:", request.args)
    event = session.query(Event).get(event_id)
    ticket = session.query(Ticket).get(ticket_id)
    formatted_date = event.date.strftime('%d-%b')
    formatted_time = event.time.strftime('%H:%M')

    event_name = event.ename
    file_name = f"{event_name}_Ticket_{ticket_id}.pdf"
    file_path = f"/tmp/{file_name}"
    generate_pdf_ticket(event_name, ticket_id, file_path)

    email = ticket.email

    msg = Message("Your Ticket for {}".format(event_name),
                    recipients=[email])
    msg.body = "Here is your ticket for the event: {}".format(event_name)
    with bp.open_resource(file_path) as fp:
        msg.attach(file_name, "application/pdf", fp.read())

    current_app.extensions['mail'].send(msg)

    os.remove(file_path)

    session.close()
    
    # Pass event and ticket details to the confirmation template
    return render_template('confirm.html', event=event, ticket=ticket, formatted_date=formatted_date, formatted_time=formatted_time)

@bp.route('/qrcode/<ticket_id>')
def get_qrcode(ticket_id):
    # Retrieve the ticket from the database
    ticket = session.query(Ticket).filter_by(id=ticket_id).first()
    if ticket:
        # Return the QR code image
        return send_file(io.BytesIO(ticket.qrcode), mimetype='image/png')
    else:
        return "", 404
    
@bp.route('/emage/<event_id>')
def get_emage(event_id):
    event = session.query(Event).filter_by(id=event_id).first()
    if event:
        # Return the QR code image
        return send_file(io.BytesIO(event.emage), mimetype='image/png')
    else:
        return "", 404

@bp.route('/browse-events')
def browse_events():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        if current_user.is_authenticated:
            query = session.query(Event).filter(Event.user_id == current_user.id)
        else:
            query = session.query(Event)
        
        total_events = query.count()
        events = query.offset((page - 1) * per_page).limit(per_page).all()
        total_pages = ceil(total_events / per_page)
        
    except NoResultFound:
        events = []
        total_pages = 1

    return render_template('events.html', events=events, page=page, total_pages=total_pages)

@bp.route('/ticket_search', methods=['GET', 'POST'], strict_slashes=False)
def ticket_search():
    form = TiketSearchForm()
    if form.validate_on_submit():
        ticket = session.query(Ticket).filter_by(lname=form.lname.data).first()
        if ticket and ticket.email == form.email.data:
            event_id = ticket.event_id
            ticket_id=ticket.id
            return (url_for('routes.confirm_ticket', event_id=event_id, ticket_id=ticket_id))
        else:
            flash('No ticket with the provided info was found, please try again or contact our support team.', 'danger')
    return render_template('ticket-search.html', title='Search Ticket', form=form)

