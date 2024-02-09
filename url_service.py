from sqlalchemy.orm import Session
from datetime import datetime
import models
from utils import generate_short_id


def create_short_url(db: Session, url: str):
    existing_shorter = db.query(models.UrlShorten).filter(models.UrlShorten.long_url == url).first()
    if existing_shorter:
        return existing_shorter
    attempt = 0
    length = 8
    while True:
        url_id = generate_short_id(url, length, attempt)
        if not db.query(models.UrlShorten).filter(models.UrlShorten.id == url_id).first():
            db_url = models.UrlShorten(id=url_id, long_url=url)
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            return db_url
        attempt += 1


def get_short_url_by_id(db: Session, urlid: str):
    return db.query(models.UrlShorten).filter(models.UrlShorten.id == urlid).first()


def update_long_url_by_id(db: Session, url_id: str, new_url: str):
    db_url = db.query(models.UrlShorten).filter(models.UrlShorten.id == url_id).first()
    if db_url:
        db_url.long_url = new_url
        db_url.update_time = datetime.utcnow()
        db.commit()
        db.refresh(db_url)
        return db_url
    else:
        return None


def delete_short_url(db: Session, url_id: int):
    db_url = db.query(models.UrlShorten).filter(models.UrlShorten.id == url_id).first()
    if db_url:
        db.delete(db_url)
        db.commit()
        return True
    else:
        return False


def get_all_short_urls(db: Session):
    return db.query(models.UrlShorten).all()


def delete_all_short_urls(db: Session):
    try:
        db.query(models.UrlShorten).delete()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
        return False
    finally:
        db.close()
