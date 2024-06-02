#!/usr/bin/python3
""" Event Class"""
import models
from .base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Date, Time, Integer, Text, func
from sqlalchemy.orm import relationship
import uuid

class Event(Base, BaseModel):
    """Representation of an event"""
    __tablename__ = 'events'
    id = Column(String(60), primary_key=True, default=uuid.uuid4)
    ename = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    venue = Column(String(255), nullable=False)
    places = Column(Integer, nullable=False)
    details = Column(Text, nullable=False)
    t_price = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    tickets = relationship("Ticket", back_populates="event")
    user = relationship("User", back_populates="events")

    
    def __init__(self, ename="", date=None, time=None, venue="", places=0, details="", t_price=0, user_id=""):
        """Initializes an event"""
        super().__init__()
        self.ename = ename
        self.date = date
        self.time = time
        self.venue = venue
        self.places = places
        self.details = details
        self.t_price = t_price
        self.user_id = user_id

