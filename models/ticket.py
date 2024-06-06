from .base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
import qrcode
import io

class Ticket(BaseModel):
    """Representation of a ticket"""
    __tablename__ = 'tickets'

    # Define the 'fname' column as a string with a maximum length of 60 characters, set it as not nullable
    fname = Column(String(60), nullable=False)
    
    # Define the 'lname' column as a string with a maximum length of 60 characters, set it as not nullable
    lname = Column(String(60), nullable=False)
    
    # Define the 'email' column as an email type, set it as not nullable
    email = Column(EmailType, nullable=False)
    
    # Define the 'pnumber' column as a string with a maximum length of 10 characters, set it as not nullable
    pnumber = Column(String(10), nullable=False)
    
    # Define the 'qrcode' column as a large binary, set it as not nullable
    qrcode = Column(LargeBinary, nullable=False)
    
    # Define the 'event_id' column as a string with a maximum length of 60 characters, set it as a foreign key to 'events.id', and set it as not nullable
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)

    # Define the relationship with the 'Event' class, set it as 'event' and back_populates as 'tickets'
    event = relationship("Event", back_populates="tickets")

    def __init__(self, fname="", lname="", email="", pnumber="", event_id=""):
        """Initializes a ticket"""
        # Call the parent class's __init__ method
        super().__init__()
        
        # Set the 'fname' attribute to the provided value
        self.fname = fname
        
        # Set the 'lname' attribute to the provided value
        self.lname = lname
        
        # Set the 'email' attribute to the provided value
        self.email = email
        
        # Set the 'pnumber' attribute to the provided value
        self.pnumber = pnumber
        
        # Set the 'event_id' attribute to the provided value
        self.event_id = event_id
        
        # Generate a QR code for the ticket
        self.qrcode = self.generate_qrcode()

    def generate_qrcode(self):
        """Generate a QR code for the ticket"""
        # Define the QR code data as a string containing the ticket ID and event ID
        qr_data = f"Ticket ID: {self.id}, Event ID: {self.event_id}"
        
        # Create a QR code object with the specified version, error correction, box size, and border
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        
        # Add the QR code data to the QR code object
        qr.add_data(qr_data)
        
        # Make the QR code
        qr.make(fit=True)
        
        # Create a QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Create a byte array to store the QR code image
        img_byte_arr = io.BytesIO()
        
        # Save the QR code image to the byte array
        img.save(img_byte_arr, format='PNG')
        
        # Seek the byte array to the beginning
        img_byte_arr.seek(0)
        
        # Return the QR code image as a byte array
        return img_byte_arr.read()