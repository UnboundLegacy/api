from sqlalchemy import BigInteger, Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, LargeBinary, String, \
    Text, Date
from sqlalchemy import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import FetchedValue
from sqlalchemy.sql import select
from sqlalchemy.orm import relationship

from . import Base


class ModelMixIn:
    def to_dict(self, **kwargs):
        if 'columns' in kwargs:
            return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name in kwargs['columns']}
        else:
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    def update_from_dict(self, json_dict):
        for key, value in json_dict.items():
            setattr(self, key, value)

class User(Base, ModelMixIn):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(32))


class PendingUser(Base, ModelMixIn):
    __tablename__ = 'pending_user'

    pending_user_id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    is_approved = Column(Boolean)
    invite_code = Column(String(255))


class Address(Base, ModelMixIn):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True)
    first_line = Column(String(255))
    second_line = Column(String(255))

class Education(Base, ModelMixIn):
    __tablename__ = 'education'

    education_id = Column(Integer, primary_key=True)

class Job(Base, ModelMixIn):
    __tablename__ = 'job'

    job_id = Column(Integer, primary_key=True)
