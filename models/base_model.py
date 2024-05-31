#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from . import engine, Session
import uuid

SQLALCHEMY_DATABASE_URI = 'sqlite:///tickety.db'
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    __tablename__ = 'base_model'
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at") and isinstance(kwargs["created_at"], str):
                self.created_at = datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at") and isinstance(kwargs["updated_at"], str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id") is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = new_dict["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["updated_at"] = new_dict["updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None and "password" in new_dict:
            del new_dict["password"]
        return new_dict
    
    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        from . import Session  # Importing Session locally to avoid circular imports
        session = Session()
        session.add(self)
        session.commit()
        session.close()

    def delete(self):
        """delete the current instance from the storage"""
        from . import Session  # Importing Session locally to avoid circular imports
        session = Session()
        session.delete(self)
        session.commit()
        session.close()