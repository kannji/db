from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .Base import Base, dbURL


db_engine = create_engine(dbURL)

Base.metadata.create_all(db_engine)

SessionFactory = sessionmaker(bind=db_engine)
session = SessionFactory()

