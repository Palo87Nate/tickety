from .base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
import qrcode
import io

class Ticket(BaseModel):
    """Representation of a ticket"""
    __tablename__ = 'tickets'
    fname = Column(String(60), nullable=False)    
    lname = Column(String(60), nullable=False)
    email = Column(EmailType, nullable=False)
    pnumber = Column(String(10), nullable=False)
    qrcode = Column(LargeBinary, nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    event = relationship("Event", back_populates="tickets")

    def __init__(self, fname="", lname="", email="", pnumber="", event_id=""):
        """Initializes a ticket"""
        super().__init__()
        self.fname = fname
        self.lname = lname
        self.email = email
        self.pnumber = pnumber
        self.event_id = event_id
        self.qrcode = self.generate_qrcode()

    def generate_qrcode(self):
        """Generate a QR code for the ticket"""
        qr_data = f"Ticket ID: {self.id}, Event ID: {self.event_id}"
    
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create a QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return img_byte_arr.read()