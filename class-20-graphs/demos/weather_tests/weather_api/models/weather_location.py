from sqlalchemy.orm import relationship
from sqlalchemy.exc import DBAPIError
from datetime import datetime as dt
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    ForeignKey,
)


from .meta import Base


class WeatherLocation(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    zip_code = Column(Integer, unique=True, nullable=False)

    date_created = Column(DateTime, default=dt.now())
    date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())

    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    accounts = relationship('Account', back_populates='location')

    @classmethod
    def new(cls, request=None, **kwargs):
        if request.dbsession is None:
            raise DBAPIError

        # weather = WeatherLocation({'name': 'some name', 'zip_code': 98038})
        weather = cls(**kwargs)
        request.dbsession.add(weather)

        return request.dbsession.query(cls).filter(
            cls.zip_code == kwargs['zip_code']).one_or_none()

    @classmethod
    def all(cls, request=None):
        if request.dbsession is None:
            raise DBAPIError

        return request.dbsession.query(cls).all()

    @classmethod
    def one(cls, request=None, pk=None):
        if request.dbsession is None:
            raise DBAPIError

        return request.dbsession.query(cls).get(pk)

    @classmethod
    def remove(cls, request=None, pk=None):
        if request.dbsession is None:
            raise DBAPIError

        return request.dbsession.query(cls).filter(
            cls.accounts.email == request.authenticated_userid
        ).filter(cls.id == pk).delete()
