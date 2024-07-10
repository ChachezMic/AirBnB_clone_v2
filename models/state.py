#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import os

HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    if (HBNB_TYPE_STORAGE == 'db'):
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City',
            back_populates='state',
            cascade='all, delete'
            )

    if (HBNB_TYPE_STORAGE != 'db'):
        @property
        def cities(self):
            """get list of city objects in this state"""
            from models.__init__ import storage
            from models.city import City
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return (city_list)
