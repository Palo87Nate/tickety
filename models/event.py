#!/usr/bin/python3
""" Event Class"""
import models
from .base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
import uuid

class Event(Base, BaseModel):
    """Representation of an event"""
    __tablename__ = 'events'
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False,  unique=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    venue = Column(String(255), nullable=False)
    tickets = relationship("Ticket", back_populates="event")
    
    def __init__(self, name="", date=None, time=None, venue=""):
        """Initializes an event"""
        super().__init__()
        self.name = name
        self.date = date
        self.time = time
        self.venue = venue

