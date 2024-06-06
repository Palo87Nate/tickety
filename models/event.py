from.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Date, Time, Integer, Text
from sqlalchemy.orm import relationship

class Event(BaseModel):
    """Representation of an event"""
    __tablename__ = 'events'

    # Define the 'ename' column as a string with a maximum length of 255 characters, set it as not nullable
    ename = Column(String(255), nullable=False)
    
    # Define the 'date' column as a date, set it as not nullable
    date = Column(Date, nullable=False)
    
    # Define the 'time' column as a time, set it as not nullable
    time = Column(Time, nullable=False)
    
    # Define the 'enue' column as a string with a maximum length of 255 characters, set it as not nullable
    venue = Column(String(255), nullable=False)
    
    # Define the 'places' column as an integer, set it as not nullable
    places = Column(Integer, nullable=False)
    
    # Define the 'details' column as a text, set it as not nullable
    details = Column(Text, nullable=False)
    
    # Define the 't_price' column as an integer, set it as not nullable
    t_price = Column(Integer, nullable=False)
    
    # Define the 'user_id' column as a string with a maximum length of 60 characters, set it as a foreign key to 'users.id', and set it as not nullable
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    # Define the relationship with the 'Ticket' class, set it as 'tickets' and back_populates as 'event'
    tickets = relationship("Ticket", back_populates="event")
    
    # Define the relationship with the 'User' class, set it as 'user' and back_populates as 'events'
    user = relationship("User", back_populates="events")

    def __init__(self, ename="", date=None, time=None, venue="", places=0, details="", t_price=0, user_id=""):
        """Initializes an event"""
        # Call the parent class's __init__ method
        super().__init__()
        
        # Set the 'ename' attribute to the provided value
        self.ename = ename
        
        # Set the 'date' attribute to the provided value
        self.date = date
        
        # Set the 'time' attribute to the provided value
        self.time = time
        
        # Set the 'enue' attribute to the provided value
        self.venue = venue
        
        # Set the 'places' attribute to the provided value
        self.places = places
        
        # Set the 'details' attribute to the provided value
        self.details = details
        
        # Set the 't_price' attribute to the provided value
        self.t_price = t_price
        
        # Set the 'user_id' attribute to the provided value
        self.user_id = user_id