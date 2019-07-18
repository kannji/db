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

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    type = Column(EnumColumn(EdgeTypes))

    source_node = Column(UUID(as_uuid=True), ForeignKey('node.uuid'), primary_key=True)
    target_node = Column(UUID(as_uuid=True), ForeignKey('node.uuid'), primary_key=True)

    source = relationship("Node", back_populates="targets")
    target = relationship("Node", back_populates="sources")


class Node(Base):

    __tablename__ = 'node'

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    content = Column(String)

    sources = relationship("Edge", back_populates="target")
    targets = relationship("Edge", back_populates="source")

