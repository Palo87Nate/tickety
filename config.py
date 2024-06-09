#!/usr/bin/python3
from .routes import bp
class Config:
    SECRET_KEY = '870198AO72ZN63'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'nathannkweto87@gmail.com'
    MAIL_PASSWORD = 'aomwdfkkpzyiondp'
    MAIL_DEFAULT_SENDER = 'nathannkweto87@gmail.com'
    MAIL_DEBUG = True
