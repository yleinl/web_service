import sqlite3


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
    :param conn: database connection
    :param user: user object
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


def register_user(username, password):
    """
    Register a new user with the given username and password.
    If the username already exists, return 409 (Conflict).
    If the registration is successful, return 201 (Created).
    :param username: The username for the new user.
    :param password: The password for the new user.
    :return: An HTTP status code indicating the result of the registration attempt.
             201 for successful registration, 409 if the username already exists,
             400 for database errors or inability to create a database connection.
    """
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


# user login
def user_login(username, password):
    """
    Attempt to authenticate a user based on the provided username and password.
    :param username: The username to authenticate.
    :param password: The password associated with the username.
    :return: An HTTP status code indicating the result of the login attempt.
             200 for successful login, 403 for incorrect password, or username not found,
             400 for database errors or inability to create a database connection.
    """
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


def password_change(username, password):
    """
    Attempt to change the password of the specified user.
    :param username: The username whose password needs to be changed.
    :param password: The new password for the user.
    :return: An HTTP status code indicating the result of the password change attempt.
             200 for successful password change, 403 if the username doesn't exist,
             400 for database errors or inability to create a database connection.
    """
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
