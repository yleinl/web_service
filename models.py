from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Inherit model base class to map to database
Base = declarative_base()


class UrlShorten(Base):
    # specify table name
    __tablename__ = 'url_shorten'

    id = Column(String(255), primary_key=True)

    # The maximum length of url in chrome is 2083
    long_url = Column(String(2083), nullable=False)

    def __repr__(self):
        return f"<url_shorten(id={self.id}, long_url='{self.url}', create_time={self.create_time}, update_time={self.update_time})>"
