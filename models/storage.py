from .base_model import BaseModel, engine
from .user import User
from .event import Event
from .ticket import Ticket
from sqlalchemy.orm import sessionmaker

# Create a session maker bound to the engine
Session = sessionmaker(bind=engine)

# Create all tables in the database
BaseModel.metadata.create_all(engine)

def register(name, email, pnumber):
    """Create a new user"""
    # Create a new session
    session = Session()
    
    try:
        # Create a new user with the provided name, email, and phone number
        user = User(name=name, email=email, pnumber=pnumber)
        
        # Add the user to the session
        session.add(user)
        
        # Commit the session
        session.commit()
        
        # Return the created user
        return user
    except Exception as e:
        # Roll back the session if an exception occurs
        session.rollback()
        
        # Raise the exception
        raise e
    finally:
        # Close the session
        session.close()

def create_event(ename, date, time, venue, places, details, t_price, user_id):
    """Create a new event"""
    # Create a new session
    session = Session()
    
    try:
        # Create a new event with the provided event name, date, time, venue, places, details, ticket price, and user ID
        event = Event(ename=ename, date=date, time=time, venue=venue, places=places, details=details, t_price=t_price, user_id=user_id)
        
        # Add the event to the session
        session.add(event)
        
        # Commit the session
        session.commit()
        
        # Return the created event
        return event
    except Exception as e:
        # Roll back the session if an exception occurs
        session.rollback()
        
        # Raise the exception
        raise e
    finally:
        # Close the session
        session.close()

def buy_ticket(fname, lname, email, pnumber):
    """Create a ticket"""
    # Create a new session
    session = Session()
    
    try:
        # Create a new ticket with the provided first name, last name, email, and phone number
        ticket = Ticket(fname=fname, lname=lname, email=email, pnumber=pnumber)
        
        # Add the ticket to the session
        session.add(ticket)
        
        # Commit the session
        session.commit()
        
        # Return the created ticket
        return ticket
    except Exception as e:
        # Roll back the session if an exception occurs
        session.rollback()
        
        # Raise the exception
        raise e
    finally:
        # Close the session
        session.close()

def browse_events():
    """Get all events"""
    # Create a new session
    session = Session()
    
    try:
        # Query all events from the database
        events = session.query(Event).all()
        
        # Return the queried events
        return events
    except Exception as e:
        # Roll back the session if an exception occurs
        session.rollback()
        
        # Raise the exception
        raise e
    finally:
        # Close the session
        session.close()

def get_user_events(user_id):
    """Get all events for a specific user"""
    # Create a new session
    session = Session()
    
    try:
        # Query all events for the user with the provided user ID
        events = session.query(Event).filter(Event.user_id == user_id).all()
        
        # Return the queried events
        return events
    except Exception as e:
        # Roll back the session if an exception occurs
        session.rollback()
        
        # Raise the exception
        raise e
    finally:
        # Close the session
        session.close()