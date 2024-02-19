import json

from flask import Flask, request, jsonify
from url_service import create_short_url, get_short_url_by_id, update_long_url_by_id, delete_short_url, \
    get_all_short_urls, delete_all_short_urls
from utils import is_valid_url, JWT_Table
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
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({'value': 'forbidden'}), 403
    if request.is_json:
        data = request.json
        new_url = data.get('url')
        # user_ip = request.remote_addr
        if not new_url:
            return jsonify({'error': 'parameter invalid', 'value': 'error'}), 400
        # check first to pass the test
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid', 'value': 'error'}), 400
        res = update_long_url_by_id(url_id, new_url, authorization_header)
        if res:
            return jsonify({'url': new_url}), 200
        else:
            return jsonify({'error': 'url id update not permitted'}), 403
    else:
        # as the request type in tester is not json, but a string
        data = json.loads(request.data.decode('utf-8'))
        new_url = data.get('url')
        if not new_url:
            return jsonify({'error': 'parameter invalid', 'value': 'error'}), 400

        # user_ip = request.remote_addr
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid', 'value': 'error'}), 400
        res = update_long_url_by_id(url_id, new_url, authorization_header)
        if res:
            return jsonify({'url': new_url}), 200
        else:
            return jsonify({'error': 'url id update not permitted'}), 403


@app.route('/<url_id>', methods=['DELETE'])
def delete_long_url(url_id):
    """
    Deletes a short URL entry by its ID.
    Returns a 204 status code on successful deletion, or a 404 if the ID does not exist.
    """
    # user_ip = request.remote_addr
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({'value': 'forbidden'}), 403
    res = delete_short_url(url_id, authorization_header)
    if res == 204:
        return jsonify({'message': 'delete success'}), 204
    elif res == 404:
        return jsonify({'error': 'url id not found'}), 404
    else:
        return jsonify({'error': 'url delete not permitted'}), 403


@app.route('/', methods=['GET'])
def get_all():
    """
    Retrieves all stored short URLs and their original counterparts.
    Returns a 200 status code with all URLs, or 404 with no url in memory.
    """
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({'value': 'forbidden'}), 403
    short_urls = get_all_short_urls(authorization_header)
    if short_urls == -1:
        return jsonify({'value': 'forbidden'}), 403
    elif not short_urls:
        return jsonify({'value': None}), 403
    else:
        value = "\n".join([f"ID: {url['id']}, Long URL: {url['long_url']}, Created by: {url['username']} \n" for url in short_urls])
        return jsonify({'value': value}), 200


@app.route('/', methods=['POST'])
def create_url_shorten():
    """
    Creates a new short URL object for the given original URL.
    Returns a 201 status code with the new short URL ID on success, or 400 with invalid parameter(format or params).
    """
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({'value': 'forbidden'}), 403
    if request.is_json:
        # user_ip = request.remote_addr
        data = request.json
        url = data.get('value')
        if not url:
            return jsonify({'error': 'parameter invalid', 'value': 'error'}), 400
        if not is_valid_url(url):
            return jsonify({'error': 'url invalid', 'value': 'error'}), 400
        length = data.get('length', 5)  # Use 5 as default if 'length' is not provided
        if not isinstance(length, int) or length <= 0:
            return jsonify({'error': 'length invalid', 'value': 'error'}), 400
        length = int(length)
        try:
            res = create_short_url(url, authorization_header, length)
            if res:
                return jsonify({'id': res['id']}), 201
            else:
                return jsonify({'value': 'forbidden'}), 403
        except Exception as e:
            return jsonify({'error': str(e), 'value': 'error'}), 400
    else:
        return jsonify({'error': 'parameter incorrect', 'value': 'error'}), 400


@app.route('/', methods=['DELETE'])
def delete_all():
    """
    Deletes all short URL entries from the database.
    Returns a 404 status code to indicate all entries have been successfully deleted.
    """
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({'value': 'forbidden'}), 403
    res = delete_all_short_urls(authorization_header)
    if res == 404:
        return '', 404
    else:
        return jsonify({'value': 'forbidden'}), 403


trust_source = ['127.0.0.1']


@app.route("/authorization", methods=["POST"])
def handle_notification():
    if request.remote_addr not in trust_source:
        return "Not Found", 404
    data = request.get_json()
    jwt_token = data.get("jwt")
    username = data.get("username")
    JWT_Table[jwt_token] = username
    return "authorization received", 200


if __name__ == '__main__':
    app.run(port=5000)
    # app.run(host='0.0.0.0', port=5000)