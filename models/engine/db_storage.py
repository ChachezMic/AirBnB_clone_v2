#!/usr/bin/python3
"""Module handling database storage"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

# Set these temporarily in __init__ file for testing and development
HBNB_ENV = os.getenv('HBNB_ENV')
HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')


classes = {
            'State': State,
            'City': City,
            'User': User,
            'Place': Place,
            'Review': Review,
            'Amenity': Amenity
          }


class DBStorage:
    """Class defining database storage object"""

    __engine = None
    __session = None

    def __init__(self):
        """function to run during DBstorage instance creation"""
        conn = "mysql+mysqldb://{}:{}@{}/{}".format(
            HBNB_MYSQL_USER,
            HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST,
            HBNB_MYSQL_DB
        )
        self.__engine = create_engine(conn, pool_pre_ping=True, echo=False)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Bring database into application as objects"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def new(self, obj):
        """Add object to current session"""
        self.__session.add(obj)

    def save(self):
        """Save to database"""
        self.__session.commit()

    def delete(self, obj):
        """delete object from current session"""
        self.__session.delete(obj)
        self.save()

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        results = {}
        if cls is None:
            for k, v in classes.items():
                objs = self.__session.query(v).all()
                for obj in objs:
                    results["{}.{}".format(k, obj.id)] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                results["{}.{}".format(cls, obj.id)] = obj
        return results

    def close(self):
        """calls restore reload the session"""
        self.__session.close()
        self.reload()
