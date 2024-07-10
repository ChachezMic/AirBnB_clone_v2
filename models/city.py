#!/usr/bin/python3
"""This is the city class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column,Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """This is the class for City
    Attributes:
        state_id: The state id
        name: input name
    """
    # initialize class for file/db storage type
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    state = relationship('State', back_populates='cities')
    places = relationship('Place', cascade='all, delete-orphan', backref='cities')
