from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from . import Session

# Define the SQLALCHEMY_DATABASE_URI variable to specify the database connection
SQLALCHEMY_DATABASE_URI = 'sqlite:///tickety.db'

# Create a database engine using the SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

class BaseModel(Base):
    """The BaseModel class from which future classes will be derived"""
    __abstract__ = True

    # Define the 'id' column as a string with a maximum length of 60 characters, 
    # set it as the primary key, and assign a default value using uuid.uuid4()
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Define the 'created_at' column as a datetime, set a default value to the current UTC time
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define the 'updated_at' column as a datetime, set a default value to the current UTC time, 
    # and update it automatically when the row is updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)

    def __str__(self):
        """String representation of the BaseModel class"""
        # Return a string representation of the instance, including its class name and id
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        # Create a copy of the instance's dictionary
        new_dict = self.__dict__.copy()
        
        # Format the 'created_at' and 'updated_at' datetime objects as strings
        new_dict["created_at"] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["updated_at"] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        
        # Add the instance's class name to the dictionary
        new_dict["__class__"] = self.__class__.__name__
        
        # Remove the '_sa_instance_state' key from the dictionary
        new_dict.pop('_sa_instance_state', None)
        
        # If save_fs is None and the dictionary contains a 'password' key, remove it
        if save_fs is None and "password" in new_dict:
            del new_dict["password"]
        
        # Return the updated dictionary
        return new_dict
    
    def save(self, session):
        """updates the attribute 'updated_at' with the current datetime and commits the session"""
        # Set the session to the provided session or the default Session
        session = Session
        
        # Update the 'updated_at' attribute with the current UTC time
        self.updated_at = datetime.utcnow()
        
        # Add the instance to the session
        session.add(self)
        
        # Commit the session
        session.commit()

    def delete(self, session):
        """delete the current instance from the storage and commits the session"""
        # Set the session to the provided session or the default Session
        session = Session
        
        # Delete the instance from the session
        session.delete(self)
        
        # Commit the session
        session.commit()