from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from .models import User, Event, Ticket, Session as session, storage
from .models.storage import create_event
from .forms import RegistrationForm, LoginForm, EventForm
from sqlalchemy.orm.exc import NoResultFound
from math import ceil
import uuid

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

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
        try:
            create_event(
                ename=form.ename.data,
                date=form.date.data,
                time=form.time.data,
                venue=form.venue.data,
                places=form.places.data,
                details=form.details.data,
                t_price=form.t_price.data,
                user_id=current_user.id
            )
            flash('Event created successfully!', 'success')
            return redirect(url_for('routes.browse_events'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
    
    return render_template('event.html', form=form, cache_id=uuid.uuid4())

@bp.route('/browse-events')
def browse_events():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        if current_user.is_authenticated:
            query = session.query(Event).filter(Event.user_id == current_user.id)
        else:
            query = Event.query
        
        total_events = query.count()
        events = query.offset((page - 1) * per_page).limit(per_page).all()
        total_pages = ceil(total_events / per_page)
        
    except NoResultFound:
        events = []
        total_pages = 1

    return render_template('events.html', events=events, page=page, total_pages=total_pages)
