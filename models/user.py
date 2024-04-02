#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            passwd = kwargs.pop('password', None)
            if passwd:
                hashed_passwd = md5().update(
                    passwd.encode('utf-8')
                ).hexidigest()
                kwargs['password'] = hashed_passwd
        super().__init__(*args, **kwargs)
        # Hash the password if provided
        # if 'password' in kwargs and kwargs['password'] is not None:
        #   self.set_password(kwargs['password'])
