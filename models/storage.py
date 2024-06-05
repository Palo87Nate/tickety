from .base_model import BaseModel, engine
from .user import User
from .event import Event
from .ticket import Ticket
from sqlalchemy.orm import sessionmaker

# Create a session factory
Session = sessionmaker(bind=engine)
BaseModel.metadata.create_all(engine)

# Define functions using the session factory
def register(name, email, pnumber):
    """ Create a new user """
    session = Session()
    try:
        user = User(name=name, email=email, pnumber=pnumber)
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def create_event(ename, date, time, venue, places, details, t_price, user_id):
    """ Create a new event """
    session = Session()
    try:
        event = Event(ename=ename, date=date, time=time, venue=venue, places=places, details=details, t_price=t_price, user_id=user_id)
        session.add(event)
        session.commit()
        return event
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def buy_ticket(fname, lname, email, pnumber):
    """ Create a ticket """
    session = Session()
    try:
        ticket = Ticket(fname=fname, lname=lname, email=email, pnumber=pnumber)    
        session.add(ticket)
        session.commit()
        return ticket
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def browse_events():
    """ Get all events """
    session = Session()
    try:
        events = session.query(Event).all()
        return events
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_events(user_id):
    session = Session()
    try:
        events = session.query(Event).filter(Event.user_id == user_id).all()
        return events
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
