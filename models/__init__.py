#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Define your database connection here
SQLALCHEMY_DATABASE_URI = 'sqlite:///tickety.db'

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create a Session class bound to the engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Import all models here
from .base_model import Base, BaseModel
from .user import User
from .event import Event
from .ticket import Ticket

# Create all tables in the database
Base.metadata.create_all(engine)
