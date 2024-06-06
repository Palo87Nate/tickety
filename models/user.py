from .base_model import BaseModel
from . import Session as session
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    """Representation of a user"""
    __tablename__ = 'users'

    # Define the 'name' column as a string with a maximum length of 255 characters, set it as not nullable and unique
    name = Column(String(255), nullable=False, unique=True)
    
    # Define the 'password' column as a string with a maximum length of 255 characters, set it as not nullable
    password = Column(String(255), nullable=False)
    
    # Define the 'email' column as an email type, set it as not nullable and unique
    email = Column(String(255), nullable=False, unique=True)
    
    # Define the 'pnumber' column as a string with a maximum length of 10 characters, set it as not nullable
    pnumber = Column(String(10), nullable=False)
    
    # Define the 'events' relationship with the 'Event' class, set it as 'events' and back_populates as 'user'
    events = relationship("Event", back_populates="user")

    def __init__(self, name="", password=None, email=None, pnumber=None):
        """Initializes a user"""
        # Call the parent class's __init__ method
        super().__init__()
        
        # Set the 'name' attribute to the provided value
        self.name = name
        
        # Set the 'password' attribute to the provided value, hashed using the set_password method
        if password:
            self.set_password(password)
        
        # Set the 'email' attribute to the provided value
        self.email = email
        
        # Set the 'pnumber' attribute to the provided value
        self.pnumber = pnumber

    def set_password(self, password):
        """Sets the password hash for the user"""
        # Generate a password hash using the provided password
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash"""
        # Check if the provided password matches the stored hash
        return check_password_hash(self.password, password)

    def is_active(self):
        """Returns True, indicating that the user is active"""
        # Return True, indicating that the user is active
        return True

    def get_id(self):
        """Returns the unique identifier for the user"""
        # Return the unique identifier for the user as a string
        return str(self.id)

    def is_authenticated(self):
        """Returns True, indicating that the user is authenticated"""
        # Return True, indicating that the user is authenticated
        return 'authenticated' in session