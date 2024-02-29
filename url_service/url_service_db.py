from utils import generate_short_id, is_jwt_expired, validate_jwt
import threading
import sqlite3

def init_db():
    conn = sqlite3.connect('./db/user_auth.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS short_urls (
            url_id TEXT PRIMARY KEY,
            long_url TEXT NOT NULL,
            username TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

lock = threading.Lock()
MAX_ATTEMPTS = 1000

def create_short_url(url: str, authorization_header: str, id_length: int):
    if not validate_jwt(authorization_header) or is_jwt_expired(authorization_header):
        return None
    username = validate_jwt(authorization_header)

    conn = sqlite3.connect('./db/user_auth.db')
    cursor = conn.cursor()

    for attempt in range(MAX_ATTEMPTS):
        url_id = generate_short_id(url, id_length, attempt)
        cursor.execute('SELECT url_id FROM short_urls WHERE url_id = ?', (url_id,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO short_urls (url_id, long_url, username) VALUES (?, ?, ?)',
                           (url_id, url, username))
            conn.commit()
            conn.close()
            return {'id': url_id, 'long_url': url, 'username': username}

    conn.close()
    raise Exception("Failed to generate a unique short ID after maximum attempts.")

def get_short_url_by_id(urlid: str):
    conn = sqlite3.connect('./db/user_auth.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url_id, long_url, username FROM short_urls WHERE url_id = ?', (urlid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'id': row[0], 'long_url': row[1], 'username': row[2]}
    else:
        return None

def update_long_url_by_id(url_id: str, new_url: str, authorization_header: str):
    if not validate_jwt(authorization_header) or is_jwt_expired(authorization_header):
        return None
    username = validate_jwt(authorization_header)

    conn = sqlite3.connect('./db/user_auth.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM short_urls WHERE url_id = ?', (url_id,))
    row = cursor.fetchone()
    if row and row[0] == username:
        with lock:
            cursor.execute('UPDATE short_urls SET long_url = ? WHERE url_id = ?', (new_url, url_id))
            conn.commit()
        conn.close()
        return {'id': url_id, 'long_url': new_url, 'username': username}
    else:
        conn.close()
        return None

def delete_short_url(url_id: str, authorization_header: str):
    if not validate_jwt(authorization_header) or is_jwt_expired(authorization_header):
        return 403
    username = validate_jwt(authorization_header)
    conn = sqlite3.connect('./db/user_auth.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM short_urls WHERE url_id = ?', (url_id,))
    row = cursor.fetchone()

    if row:
        if row[0] != username:
            return 403
        with lock:
            cursor.execute('DELETE FROM short_urls WHERE url_id = ?', (url_id,))
            conn.commit()
        conn.close()
        return 204
    else:
        conn.close()
        return 404

def get_all_short_urls(authorization_header: str):
    if not validate_jwt(authorization_header) or is_jwt_expired(authorization_header):
        return 403

    conn = sqlite3.connect('./db/user_auth.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url_id, long_url, username FROM short_urls')
    urls = [{'id': row[0], 'long_url': row[1], 'username': row[2]} for row in cursor.fetchall()]
    conn.close()
    return urls

def delete_all_short_urls(authorization_header: str):
    if not validate_jwt(authorization_header) or is_jwt_expired(authorization_header):
        return 403

    conn = sqlite3.connect('./db/user_auth.db')
    with lock:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM short_urls')
        conn.commit()
    conn.close()
    return 404
