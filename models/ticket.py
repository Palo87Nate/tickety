#!/usr/bin/python
"""The Ticket"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import qrcode
import base64
import io
from io import BytesIO

class Ticket(Base, BaseModel):
    """Representation of a ticket"""
    __tablename__ = 'tickets'
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_name = Column(String(60), ForeignKey('events.name'), nullable=False)
    #ticket_number = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    qrcode = Column(String(500), nullable=False)
    event = relationship("Event", back_populates="tickets")

    def __init__(self, event_name="", price=None):
        """Initializes a ticket"""
        super().__init__()
        self.id = str(uuid.uuid4())
        self.event_name = event_name
        #self.ticket_number = ticket_number
        self.price = price
        self.qrcode = self.generate_qrcode()

    def generate_qrcode(self):
        """Generate a QR code for the ticket"""
        qr_data = f"Ticket ID: {self.id}, Event: {self.event_name}, Price: {self.price}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image to a byte buffer
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.read()