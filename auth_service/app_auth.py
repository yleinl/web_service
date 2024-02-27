from flask import Flask, request, jsonify

# from url_service import utils
from auth import register_user, user_login, password_change, JWT_table
from auth_util import JWT_generate, notify_url_service

app = Flask(__name__)


# add authentication part


# user creation
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
            return jsonify({'detail': 'parameter invalid'}), 400
        # check if the username exists
        # if not, create a new user
        # if exists, return 409
        status_code = register_user(username, password)
        if status_code == 201:
            return jsonify({'id': username}), 201
        elif status_code == 400:
            return jsonify({'detail': 'database error'}), 400
        else:
            return jsonify({'detail': 'duplicate'}), 409
    else:
        return jsonify({'detail': 'parameter incorrect'}), 400


# user login
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
            return jsonify({'detail': 'parameter invalid'}), 400
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
            notify_url_service(JWT_token, username)
            return jsonify({'token': JWT_token}), 200
        elif status_code == 400:
            return jsonify({'detail': 'database error'}), 400
        else:
            return jsonify({'detail': 'forbidden'}), 403
    else:
        return jsonify({'detail': 'parameter incorrect'}), 400


# user change password
@app.route('/users', methods=['PUT'])
def change_password():
    """
    Change the password for a user with username and password
    If the username and password match, return a 200 status code with the new user ID on success, or 403 with incorrect username or password, or 400 with invalid parameter(format or params).
    """
    if request.is_json:
        data = request.json
        username = data.get('username')
        old_password = data.get('password')
        new_password = data.get('new_password')
        if not username or not old_password or not new_password:
            return jsonify({'detail': 'parameter invalid'}), 400
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
                return jsonify({'detail': 'database error'}), 400
            else:
                # cannot reach here in normal situation, just in case
                return jsonify({'detail': 'forbidden'}), 403
        elif status_code == 400:
            return jsonify({'detail': 'database error'}), 400
        else:
            return jsonify({'detail': 'forbidden'}), 403
    else:
        return jsonify({'detail': 'parameter incorrect'}), 400


if __name__ == '__main__':
    # app.run(port=5001)
    app.run(host='0.0.0.0', port=5001)
