#!/usr/bin/python3
""" User Class"""
import models
from .base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(Base, BaseModel):
    """Representation of an user"""
    __tablename__ = 'users'
    id = Column(String(60), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False,  unique=True)
    password = Column(String(255), nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    pnumber = Column(String(10), nullable=False)
    logo = Column(LargeBinary)
    events = relationship("Event", back_populates="user")
    
    def __init__(self, name="", password=None, email=None, pnumber=None, logo=None):
        """Initializes an event"""
        super().__init__()
        self.name = name
        if password:
            self.set_password(password)
        self.email = email
        self.pnumber = pnumber
        self.logo = logo

    def set_password(self, password):
        """Sets the password hash for the user."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)