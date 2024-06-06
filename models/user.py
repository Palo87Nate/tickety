from .base_model import BaseModel
from . import Session as session
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    """Representation of a user"""
    __tablename__ = 'users'
    name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)    
    pnumber = Column(String(10), nullable=False)    
    events = relationship("Event", back_populates="user")

    def __init__(self, name="", password=None, email=None, pnumber=None):
        """Initializes a user"""
        # Call the parent class's __init__ method
        super().__init__()        
        self.name = name        
        if password:
            self.set_password(password)        
        self.email = email        
        self.pnumber = pnumber

    def set_password(self, password):
        """Sets the password hash for the user"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash"""
        return check_password_hash(self.password, password)

    def is_active(self):
        """Returns True, indicating that the user is active"""
        return True

    def get_id(self):
        """Returns the unique identifier for the user"""
        return str(self.id)

    def is_authenticated(self):
        """Returns True, indicating that the user is authenticated"""
        return 'authenticated' in session