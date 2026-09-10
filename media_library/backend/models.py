from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key = True)
    title = Column(String)
    chapter = Column(String)
    url = Column(String)

