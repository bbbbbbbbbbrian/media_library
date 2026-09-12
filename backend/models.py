from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    series_url = Column(String)
    latest_chapter = Column(String)
    current_chapter = Column(String)
    current_url = Column(String)