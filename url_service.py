from sqlalchemy.orm import Session
import models
from utils import generate_short_id


def create_short_url(db: Session, url: str):
    """
    Checks if a short URL for the given long URL already exists. If not,
    generates a unique short ID and creates a new short URL entry in the database.

    :param db: Database session for executing queries.
    :param url: The given URL to be shortened.
    :return: The existing or newly created short URL object.
    """
    # check if the short url object already exist, if true, return it
    existing_shorter = db.query(models.UrlShorten).filter(models.UrlShorten.long_url == url).first()
    if existing_shorter:
        return existing_shorter
    attempt = 0
    length = 8
    while True:
        url_id = generate_short_id(url, length, attempt)
        # detect collision
        if not db.query(models.UrlShorten).filter(models.UrlShorten.id == url_id).first():
            db_url = models.UrlShorten(id=url_id, long_url=url)
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            return db_url
        # concatenate the attempt number to avoid collision
        attempt += 1


def get_short_url_by_id(db: Session, urlid: str):
    """
        Retrieves a short URL object by its URL ID.

        :param db: Database session for executing queries.
        :param urlid: The URL ID of the short URL.
        :return: The short URL object if found, else None.
    """
    return db.query(models.UrlShorten).filter(models.UrlShorten.id == urlid).first()


def update_long_url_by_id(db: Session, url_id: str, new_url: str):
    """
    Updates the long URL of an existing id in the database.

    :param db: Database session for executing queries.
    :param url_id: The URL ID to update.
    :param new_url: The new long URL to associate with the short URL.
    :return: The updated short URL object if successful, else None.
    """
    db_url = db.query(models.UrlShorten).filter(models.UrlShorten.id == url_id).first()
    if db_url:
        db_url.long_url = new_url
        db.commit()
        db.refresh(db_url)
        return db_url
    else:
        return None


def delete_short_url(db: Session, url_id: int):
    """
    Deletes a short URL entry from the database by its URL ID.

    :param db: Database session for executing queries.
    :param url_id: The URL ID of the short URL to delete.
    :return: True if deletion was successful, else False.
    """
    db_url = db.query(models.UrlShorten).filter(models.UrlShorten.id == url_id).first()
    if db_url:
        db.delete(db_url)
        db.commit()
        return True
    else:
        return False


def get_all_short_urls(db: Session):
    # Retrieves all short URL entries from the database.
    return db.query(models.UrlShorten).all()


def delete_all_short_urls(db: Session):
    # Deletes all short URL entries from the database.
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
