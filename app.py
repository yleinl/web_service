import json

from flask import Flask, request, jsonify
from url_service import create_short_url, get_short_url_by_id, update_long_url_by_id, delete_short_url, \
    get_all_short_urls, delete_all_short_urls
from utils import is_valid_url
from auth import regeister_user, user_login, JWT_generate, password_change, JWT_table
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
        return jsonify({'error': 'authorization required'}), 403
    if request.is_json:
        data = request.json
        new_url = data.get('url')
        # user_ip = request.remote_addr
        if not new_url:
            return jsonify({'error': 'parameter invalid'}), 400
        # check first to pass the test
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid'}), 400
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
            return jsonify({'error': 'parameter invalid'}), 400

        # user_ip = request.remote_addr
        if not get_short_url_by_id(url_id):
            return jsonify({'error': 'url id not found'}), 404
        if not is_valid_url(new_url):
            return jsonify({'error': 'url invalid'}), 400
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
        return jsonify({'error': 'authorization required'}), 403
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
        return jsonify({'error': 'authorization required'}), 403
    short_urls = get_all_short_urls(authorization_header)
    if short_urls:
        value = "\n".join([f"ID: {url['id']}, Long URL: {url['long_url']}, Created by: {url['username']} \n" for url in short_urls])
        return jsonify({'value': value}), 200
    else:
        return jsonify({'message': 'autorization failed'}), 403


@app.route('/', methods=['POST'])
def create_url_shorten():
    """
    Creates a new short URL object for the given original URL.
    Returns a 201 status code with the new short URL ID on success, or 400 with invalid parameter(format or params).
    """
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({'error': 'authorization required'}), 403
    if request.is_json:
        # user_ip = request.remote_addr
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
        try:
            res = create_short_url(url, authorization_header, length)
            if res:
                return jsonify({'id': res['id']}), 201
            else:
                return jsonify({'error': 'autorization failed'}), 403
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'parameter incorrect'}), 400


@app.route('/', methods=['DELETE'])
def delete_all():
    """
    Deletes all short URL entries from the database.
    Returns a 404 status code to indicate all entries have been successfully deleted.
    """
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        return jsonify({'error': 'authorization required'}), 403
    delete_all_short_urls(authorization_header)
    return '', 404

# add authentication part


#user creation
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user with username and password and store it in a table
    Return a 201 status code with the new user ID on success, or 409 with duplicate username, or 400 with invalid parameter(format or params).
    """
    if request.is_json:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'parameter invalid'}), 400
        # check if the username exists
        # if not, create a new user
        # if exists, return 409
        status_code = regeister_user(username, password)
        if status_code == 201:
            return jsonify({'id': username}), 201
        elif status_code == 400:
            return jsonify({'error': 'database error'}), 400
        else:
            return jsonify({'error': 'username exists'}), 409
    else:
        return jsonify({'error': 'parameter incorrect'}), 400


#user login
@app.route('/users/login', methods=['POST'])
def login_user():
    """
    Login a user with username and password
    If the username and password match, return a 200 status code with JWT token, or 403 with incorrect username or password, or 400 with invalid parameter(format or params).
    """
    if request.is_json:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'parameter invalid'}), 400
        # check if the username exists
        # if not, return 403
        # if exists, check if the password match
        # if not, return 403
        # if match, return 200 with JWT token
        status_code = user_login(username, password)
        if status_code == 200:
            # get the request header and payload
            header = request.headers.to_wsgi_list()
            payload = request.json
            JWT_token = JWT_generate(header, payload)
            JWT_table[JWT_token] = username
            return jsonify({'token': JWT_token}), 200
        elif status_code == 400:
            return jsonify({'error': 'database error'}), 400
        else:
            return jsonify({'error': 'username or password incorrect'}), 403
    else:
        return jsonify({'error': 'parameter incorrect'}), 400


#user change password
@app.route('/users', methods=['PUT'])
def change_password():
    """
    Change the password for a user with username and password
    If the username and password match, return a 200 status code with the new user ID on success, or 403 with incorrect username or password, or 400 with invalid parameter(format or params).
    """
    if request.is_json:
        data = request.json
        username = data.get('username')
        old_password = data.get('old-password')
        new_password = data.get('new-password')
        if not username or not old_password or not new_password:
            return jsonify({'error': 'parameter invalid'}), 400
        # check if the username exists
        # if not, return 403
        # if exists, check if the password match
        # if not, return 403
        # if match, change the password
        status_code = user_login(username, old_password)
        if status_code == 200:
            status_code_inner = password_change(username, new_password)
            if status_code_inner == 200:
                return jsonify({'id': username}), 200
            elif status_code_inner == 400:
                return jsonify({'error': 'database error'}), 400
            else:
                # cannot reach here in normal situation, just in case
                return jsonify({'error': 'username or password incorrect'}), 403
        elif status_code == 400:
            return jsonify({'error': 'database error'}), 400
        else:
            return jsonify({'error': 'username or password incorrect'}), 403
    else:
        return jsonify({'error': 'parameter incorrect'}), 400

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000)