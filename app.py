import json

from flask import Flask, request, jsonify
from database import SessionLocal
from models import UrlShorten
from url_service import create_short_url, get_short_url_by_id, update_long_url_by_id, delete_short_url, \
    get_all_short_urls, delete_all_short_urls
from utils import is_valid_url

app = Flask(__name__)


# rest api and application starter, all database error return 400
@app.route('/<url_id>', methods=['GET'])
def get_long_url(url_id):
    """
    Retrieves the original (long) URL associated with the given short URL ID.
    Returns a 301 and the original URL if found, otherwise returns a 404 error.
    """
    try:
        db_session = SessionLocal()
        res = get_short_url_by_id(db_session, url_id)
        if res:
            return jsonify({'value': res.long_url}), 301
        else:
            return jsonify({'error': 'id invalid'}), 404
    except Exception as e:
        # database exception handler
        db_session.rollback()
        return jsonify({'message': 'problem in database transaction'}), 400
    finally:
        db_session.close()


@app.route('/<url_id>', methods=['PUT'])
def update_long_url(url_id):
    """
    Updates the original URL associated with the given short URL ID.
    Returns a 200 status code with the updated URL on success, or an error message with appropriate status code.
    """
    if request.is_json:
        try:
            db_session = SessionLocal()
            data = request.json
            new_url = data.get('url')
            # check whether the url id is in the database
            if not get_short_url_by_id(db_session, url_id):
                return jsonify({'error': 'url id not found'}), 404
            # check the url format
            if not is_valid_url(new_url):
                return jsonify({'error': 'url invalid'}), 400
            res = update_long_url_by_id(db_session, url_id, new_url)
            if not res:
                return jsonify({'error': 'url id not found'}), 404
            else:
                return jsonify({'url': new_url}), 200
        except Exception as e:
            db_session.rollback()
            return jsonify({'error': 'problem in database transaction'}), 400
        finally:
            db_session.close()
    else:
        # this part of code is because the request content type in the tester is not json
        data = json.loads(request.data.decode('utf-8'))
        try:
            db_session = SessionLocal()
            new_url = data.get('url')
            if not get_short_url_by_id(db_session, url_id):
                return jsonify({'error': 'id invalid'}), 404
            if not is_valid_url(new_url):
                return jsonify({'error': 'url invalid'}), 400
            res = update_long_url_by_id(db_session, url_id, new_url)
            if not res:
                return jsonify({'error': 'url not found'}), 404
            else:
                return jsonify({'url': new_url}), 200
        except Exception as e:
            print(e)
            db_session.rollback()
            return jsonify({'error': 'problem in database transaction'}), 400
        finally:
            db_session.close()


@app.route('/<url_id>', methods=['DELETE'])
def delete_long_url(url_id):
    """
    Deletes a short URL entry by its ID.
    Returns a 204 status code on successful deletion, or a 404 if the ID does not exist.
    """
    try:
        db_session = SessionLocal()
        res = delete_short_url(db_session, url_id)
        if res:
            return jsonify({'message': 'delete success'}), 204
        else:
            # do not find the url id
            return jsonify({'error': 'url id not found'}), 404
    except Exception as e:
        db_session.rollback()
        return jsonify({'message': 'problem in database transaction'}), 400
    finally:
        db_session.close()


@app.route('/', methods=['GET'])
def get_all():
    """
    Retrieves all stored short URLs and their original counterparts.
    Returns a 200 status code with all URLs, or an appropriate error message.
    """
    try:
        db_session = SessionLocal()
        short_urls = get_all_short_urls(db_session)
        value = ""
        for url in short_urls:
            # integrate the results
            value += f"ID: {url.id}, Long URL: {url.long_url}\n"
        if not short_urls:
            value = None
        return jsonify({'value': value}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'message': 'problem in database transaction'}), 400
    finally:
        db_session.close()


@app.route('/', methods=['POST'])
def create_url_shorten():
    """
    Creates a new short URL object for the given original URL.
    Returns a 201 status code with the new short URL ID on success, or an error message.
    """
    if request.is_json:
        try:
            db_session = SessionLocal()
            data = request.json
            url = data.get('value')
            # check url format
            if not is_valid_url(url):
                return jsonify({'error': 'url invalid'}), 400
            res = create_short_url(db_session, url)
            db_session.commit()
            return jsonify({'id': res.id}), 201
        except Exception as e:
            db_session.rollback()
            return jsonify({'error': 'problem in database transaction'}), 400
        finally:
            db_session.close()
    else:
        return jsonify({'error': 'parameter incorrect'}), 400


@app.route('/', methods=['DELETE'])
def delete_all():
    """
    Deletes all short URL entries from the database.
    Returns a 404 status code to indicate all entries have been successfully deleted.
    """
    try:
        db_session = SessionLocal()
        delete_all_short_urls(db_session)
        return '', 404
    except Exception as e:
        db_session.rollback()
        return jsonify({'message': 'problem in database transaction'}), 400
    finally:
        db_session.close()


if __name__ == '__main__':
    # configure the port here
    app.run(port=8000)
