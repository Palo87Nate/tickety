#!/usr/bin/python3

from models.base_model import Base, Session, engine
from models.event import Event
from models.ticket import Ticket
from models.user import User
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def register(name, email, pnumber, logo):
    """ Create a new user """
    with Session() as session:
        try:
            user = User(name=name, email=email, pnumber=pnumber, logo=logo)
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e

def create_event(ename, date, time, venue, places, details, t_price, user_id):
    """ Create a new event """
    with Session() as session:
        try:
            event = Event(ename=ename, date=date, time=time, venue=venue, places=places, details=details, t_price=t_price, user_id=user_id)
            session.add(event)
            session.commit()
            return event
        except Exception as e:
            session.rollback()
            raise e

def buy_ticket(fname, lname, email, pnumber):
    """ Create a ticket """
    with Session() as session:
        try:
            ticket = Ticket(fname=fname, lname=lname, email=email, pnumber=pnumber)    
            session.add(ticket)
            session.commit()
            return ticket
        except Exception as e:
            session.rollback()
            raise e

def browse_events():
    """ Get all events """
    with Session() as session:
        try:
            events = session.query(Event).all()
            return events
        except Exception as e:
            session.rollback()
            raise e

def get_user_events(user_id):
    with Session() as session:
        try:
            events = session.query(Event).filter(Event.user_id == user_id).all()
            return events
        except Exception as e:
            session.rollback()
            raise e