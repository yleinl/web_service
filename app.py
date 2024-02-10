import json

from flask import Flask, request, jsonify
from url_service import create_short_url, get_short_url_by_id, update_long_url_by_id, delete_short_url, \
    get_all_short_urls, delete_all_short_urls
from utils import is_valid_url

app = Flask(__name__)


# rest api and application starter, all database error return 400
@app.route('/<url_id>', methods=['GET'])
def get_long_url(url_id):
    res = get_short_url_by_id(url_id)
    if res:
        return jsonify({'value': res['long_url']}), 301
    else:
        return jsonify({'error': 'id invalid'}), 404


@app.route('/<url_id>', methods=['PUT'])
def update_long_url(url_id):
    if request.is_json:
        data = request.json
        new_url = data.get('url')
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid'}), 400
        res = update_long_url_by_id(url_id, new_url)
        if res:
            return jsonify({'url': new_url}), 200
        else:
            return jsonify({'error': 'url id not found'}), 404
    else:
        data = json.loads(request.data.decode('utf-8'))
        new_url = data.get('url')
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid'}), 400
        res = update_long_url_by_id(url_id, new_url)
        if res:
            return jsonify({'url': new_url}), 200
        else:
            return jsonify({'error': 'url id not found'}), 404


@app.route('/<url_id>', methods=['DELETE'])
def delete_long_url(url_id):
    res = delete_short_url(url_id)
    if res:
        return jsonify({'message': 'delete success'}), 204
    else:
        return jsonify({'error': 'url id not found'}), 404


@app.route('/', methods=['GET'])
def get_all():
    short_urls = get_all_short_urls()
    if short_urls:
        value = "\n".join([f"ID: {url['id']}, Long URL: {url['long_url']}" for url in short_urls])
        return jsonify({'value': value}), 200
    else:
        return jsonify({'message': 'No URLs found'}), 404


@app.route('/', methods=['POST'])
def create_url_shorten():
    if request.is_json:
        data = request.json
        url = data.get('value')
        if not is_valid_url(url):
            return jsonify({'error': 'url invalid'}), 400
        res = create_short_url(url)
        return jsonify({'id': res['id']}), 201
    else:
        return jsonify({'error': 'parameter incorrect'}), 400


@app.route('/', methods=['DELETE'])
def delete_all():
    res = delete_all_short_urls()
    if res:
        return '', 404
    else:
        return jsonify({'message': 'Error deleting URLs'}), 400


if __name__ == '__main__':
    app.run(port=8000)
