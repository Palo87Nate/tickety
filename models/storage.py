#!/usr/bin/python3
from .base_model import BaseModel, engine
from .user import User
from .event import Event
from .ticket import Ticket
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
BaseModel.metadata.create_all(engine)

def register(name, email, pnumber):
    """Create a new user"""
    # Create a new session
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

def create_event(ename, date, time, venue, places, details, t_price, user_id, emage):
    session = Session()
    
    try:
        # Create a new event with the provided details
        event = Event(ename=ename, date=date, time=time, venue=venue, places=places, details=details, t_price=t_price, user_id=user_id, emage=emage)
        session.add(event)
        session.commit()
        return event
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def buy_ticket(fname, lname, email, pnumber):
    """Create a ticket"""
    session = Session()
    
    try:
        # Create a new ticket with the provided personal details
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
    """Get all events"""
    session = Session()

    try:
        # Query all events from the database
        events = session.query(Event).all()
        return events
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()