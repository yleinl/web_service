import sqlite3
import json
import base64
import hashlib
import hmac

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    username text PRIMARY KEY,
                                    password text NOT NULL
                                ); """

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        return e


def insert_user(conn, user):
    """
    try to insert a new user
    """

    sql = ''' INSERT INTO users(username, password)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()

    return cur.lastrowid


"""
use username and password to register a user, if the username exists, return 409, else create a new user and return 201
store user information in a database
"""
def regeister_user(username, password):
    conn = create_connection('user_auth.db')
    if conn is not None:
        cursor = conn.cursor()

        cursor.execute(sql_create_users_table)

        # check if the username exists
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            print("Error! Username already exists.")
            cursor.close()
            conn.close()
            return 409
        
        # if not, create a new user
        user = (username, password)
        insert_user(conn, user)
        print("User registered successfully.")
        cursor.close()
        conn.close()
        return 201
    else:
        print("Error! cannot create the database connection.")
        return 400
    
#user login
def user_login(username, password):
    conn = create_connection('user_auth.db')
    if conn is not None:
        cursor = conn.cursor()

        try:
            # check if the username exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                if existing_user[1] == password:
                    print("User login successfully.")
                    cursor.close()
                    conn.close()
                    return 200
                else:
                    print("Error! Incorrect password.")
                    cursor.close()
                    conn.close()
                    return 403
            else:
                print("Error! Username does not exist.")
                cursor.close()
                conn.close()
                return 403
        except sqlite3.Error as e:
            print(e)
            cursor.close()
            conn.close()
            return 400
    else:
        print("Error! cannot create the database connection.")
        return 400
    
"""
generate a JWT token with the header and payload
"""
def JWT_generate(header, payload):
    """
    generate a JWT token with the header and payload
    header is a list
    payload is a dictionary
    """

    encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    secret_key = 'my_secret_key'
    signature = hmac.new(secret_key.encode(), f"{encoded_header}.{encoded_payload}".encode(), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode()

    jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    return jwt_token


def password_change(username, password):
    conn = create_connection('user_auth.db')
    if conn is not None:
        cursor = conn.cursor()

        try:
            # check if the username exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                cursor.execute("UPDATE users SET password=? WHERE username=?", (password, username))
                conn.commit()
                print("Password changed successfully.")
                cursor.close()
                conn.close()
                return 200
            else:
                print("Error! Username does not exist.")
                cursor.close()
                conn.close()
                return 403
        except sqlite3.Error as e:
            print(e)
            cursor.close()
            conn.close()
            return 400
    else:
        print("Error! cannot create the database connection.")
        return 400