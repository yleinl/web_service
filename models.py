from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UrlShorten(Base):
    __tablename__ = 'url_shorten'

    id = Column(String(255), primary_key=True)
    long_url = Column(String(512), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<url_shorten(id={self.id}, long_url='{self.url}', create_time={self.create_time}, update_time={self.update_time})>"
