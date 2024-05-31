#!/usr/bin/python
"""The Ticket"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid

class Ticket(Base, BaseModel):
    """Representation of a ticket"""
    __tablename__ = 'tickets'
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_name = Column(String(60), ForeignKey('events.name'), nullable=False)
    #ticket_number = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    #barcode = Column(String(100), nullable=False)
    event = relationship("Event", back_populates="tickets")

    def __init__(self, event_name="", price=None):
        """Initializes a ticket"""
        super().__init__()
        self.event_name = event_name
        #self.ticket_number = ticket_number
        self.price = price
        #self.barcode = barcode