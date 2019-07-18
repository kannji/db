import uuid
import datetime
from enum import Enum

from sqlalchemy import Column, String, DateTime, Enum as EnumColumn, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from .env import DB_NAME, DB_USER, DB_PASSWORD, HN_DB


# The url for connecting to our database
dbURL = 'postgresql://{user}:{password}@{host}/{dbName}'.format(
    host = HN_DB,
    dbName = DB_NAME,
    user = DB_USER,
    password = DB_PASSWORD
)

# create the base for all database classes to inherit from
Base = declarative_base()

class EdgeTypes(Enum):
    writing = 1

class Edge(Base):

    __tablename__ = 'edge'

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    type = Column(EnumColumn(EdgeTypes))

    source_uuid = Column(UUID(as_uuid=True), ForeignKey('node.uuid'), primary_key=True)
    target_uuid = Column(UUID(as_uuid=True), ForeignKey('node.uuid'), primary_key=True)

    source = relationship("Node", foreign_keys=[source_uuid], backref="outgoing_edges")
    target = relationship("Node", foreign_keys=[target_uuid], backref="incoming_edges")

class Node(Base):

    __tablename__ = 'node'

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    content = Column(String, unique=True, nullable=False)

