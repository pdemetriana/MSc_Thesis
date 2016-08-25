"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import schema, types

__all__ = ['Base', 'DBSession']

# SQLAlchemy session manager. Updated by model.init_model()
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
#Session = scoped_session(sessionmaker())

# The declarative Base
metadata = schema.MetaData()
Base = declarative_base(metadata=metadata)






