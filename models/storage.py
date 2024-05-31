#!/usr/bin/python3

from models.base_model import Base, Session, engine
from models.event import Event
from models.ticket import Ticket
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def create_ticket(event_name, date, time, venue, price):
    """ Create a new event and its ticket example """
    event = Event(name=event_name, date=date, time=time, venue=venue)
    ticket = Ticket(event_name=event_name, price=price)
    
    try:
        session.add(event)
        session.add(ticket)
        session.commit()
        return event, ticket
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_your_ticket(session):
    """ Get all tickets """
    return session.query(Ticket).all()
