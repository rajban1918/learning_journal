import datetime

# from sqlalchemy import (
#     Column,
#     Index,
#     Integer,
#     Text,
#     Unicode,
#     DateTime,
#     desc
#     )

import sqlalchemy as sa
from cryptacular.bcrypt import BCRYPTPasswordManager as Manager

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    value = sa.Column(sa.Integer)

sa.Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Entry(Base):
    __tablename__ = 'entries'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Unicode(255), unique=True, nullable=False)
    body = sa.Column(sa.UnicodeText, default=u'')
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    edited = sa.Column(sa.DateTime, default=datetime.datetime.utcnow) #utcnow is faster, w/out DST or timezones

    @classmethod
    def all(cls):
        return DBSession.query(cls).order_by(sa.desc(cls.created)).all()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(cls).get(id)

class User(Base):
    __tablename__ =  'user'
    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    name  = sa.Column(sa.Unicode(255), unique = True, nullable = False)
    password =  sa.Column(sa.Unicode(15), nullable = False)

    @classmethod
    def by_name(cls, name):
        return DBSession.query(User).filter(User.name == name).first()

    def verify_password(self, password):
        manager = Manager()
        return manager.check(self.password, password)