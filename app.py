import json

from flask import Flask, request, jsonify
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
    res = get_short_url_by_id(url_id)
    if res:
        return jsonify({'value': res['long_url']}), 301
    else:
        return jsonify({'error': 'id invalid'}), 404


@app.route('/<url_id>', methods=['PUT'])
def update_long_url(url_id):
    """
    Updates the original URL associated with the given short URL ID.
    Returns a 200 status code with the updated URL on success, or an error message with 404 id not found or 400 url invalid.
    """
    if request.is_json:
        data = request.json
        new_url = data.get('url')
        user_ip = request.remote_addr
        if not new_url:
            return jsonify({'error': 'parameter invalid'}), 400
        # check first to pass the test
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid'}), 400
        res = update_long_url_by_id(url_id, new_url, user_ip)
        if res:
            return jsonify({'url': new_url}), 200
        else:
            return jsonify({'error': 'url id update not permitted'}), 404
    else:
        # as the request type in tester is not json, but a string
        data = json.loads(request.data.decode('utf-8'))
        new_url = data.get('url')
        if not new_url:
            return jsonify({'error': 'parameter invalid'}), 400

        user_ip = request.remote_addr
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid'}), 400
        res = update_long_url_by_id(url_id, new_url, user_ip)
        if res:
            return jsonify({'url': new_url}), 200
        else:
            return jsonify({'error': 'url id not found'}), 404


@app.route('/<url_id>', methods=['DELETE'])
def delete_long_url(url_id):
    """
    Deletes a short URL entry by its ID.
    Returns a 204 status code on successful deletion, or a 404 if the ID does not exist.
    """
    user_ip = request.remote_addr
    res = delete_short_url(url_id, user_ip)
    if res:
        return jsonify({'message': 'delete success'}), 204
    else:
        return jsonify({'error': 'url id not found or delete not permitted'}), 404


@app.route('/', methods=['GET'])
def get_all():
    """
    Retrieves all stored short URLs and their original counterparts.
    Returns a 200 status code with all URLs, or 404 with no url in memory.
    """
    short_urls = get_all_short_urls()
    if short_urls:
        value = "\n".join([f"ID: {url['id']}, Long URL: {url['long_url']}, Created by: {url['user_ip']} \n" for url in short_urls])
        return jsonify({'value': value}), 200
    else:
        return jsonify({'message': 'No URLs found'}), 404


@app.route('/', methods=['POST'])
def create_url_shorten():
    """
    Creates a new short URL object for the given original URL.
    Returns a 201 status code with the new short URL ID on success, or 400 with invalid parameter(format or params).
    """
    if request.is_json:
        user_ip = request.remote_addr
        data = request.json
        url = data.get('value')
        if not url:
            return jsonify({'error': 'parameter invalid'}), 400
        if not is_valid_url(url):
            return jsonify({'error': 'url invalid'}), 400
        length = data.get('length', 5)  # Use 5 as default if 'length' is not provided
        if not isinstance(length, int) or length <= 0:
            return jsonify({'error': 'length invalid'}), 400
        length = int(length)
        res = create_short_url(url, user_ip, length)
        return jsonify({'id': res['id']}), 201
    else:
        return jsonify({'error': 'parameter incorrect'}), 400


@app.route('/', methods=['DELETE'])
def delete_all():
    """
    Deletes all short URL entries from the database.
    Returns a 404 status code to indicate all entries have been successfully deleted.
    """
    delete_all_short_urls()
    return '', 404


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000)