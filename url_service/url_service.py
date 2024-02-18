from utils import generate_short_id, JWT_Table
import threading

url_store = {}
lock = threading.Lock()

MAX_ATTEMPTS = 1000


def create_short_url(url: str, authorization_header: str, id_length: int):
    """
    Checks if a short URL ID for the given long URL already exists. If not,
    generates a new short ID and creates a new short URL entry in the memory.

    :param id_length: length of the URL
    :param user_ip: The user IP address for authorization
    :param url: The given URL to be shortened.
    :return: The existing or newly created short URL object.
    """
    if authorization_header not in JWT_Table:
        return None
    username = JWT_Table[authorization_header]
    # global url_store
    for short_id, url_info in url_store.items():
        if url_info['long_url'] == url:
            return url_info
    attempt = 0
    length = id_length
    with lock:
        for attempt in range(MAX_ATTEMPTS):
            url_id = generate_short_id(url, length, attempt)
            if url_id not in url_store:
                url_store[url_id] = {'id': url_id, 'long_url': url, 'username': username}
                return url_store[url_id]
    raise Exception("Failed to generate a unique short ID after maximum attempts.")



def get_short_url_by_id(urlid: str):
    """
    Retrieves a short URL object by its URL ID.
    :param urlid: The URL ID of the short URL.
    :return: The short URL object if found, else None.
    """
    return url_store.get(urlid, None)


def update_long_url_by_id(url_id: str, new_url: str, authorization_header: str):
    """
    Updates the long URL of an existing id in the database.

    :param username: The username for authorization
    :param url_id: The URL ID to update.
    :param new_url: The new long URL to associate with the short URL.
    :return: The updated short URL object if successful, else None.
    """
    if authorization_header not in JWT_Table:
        return None
    username = JWT_Table[authorization_header]
    if url_id in url_store:
        if url_store[url_id]['username'] != username:
            return None
        with lock:
            url_store[url_id]['long_url'] = new_url
        return url_store[url_id]
    else:
        return None


def delete_short_url(url_id: str, authorization_header: str):
    """
    Deletes a short URL entry from the database by its URL ID.
    :param username: The username for authorization
    :param url_id: The URL ID of the short URL to delete.
    :return: True if deletion was successful, else False (URL ID not found).
    """
    if authorization_header not in JWT_Table:
        return 403
    username = JWT_Table[authorization_header]
    if url_id in url_store:
        if url_store[url_id]['username'] != username:
            return 403
        with lock:
            del url_store[url_id]
        return 204
    else:
        return 404


def get_all_short_urls(authorization_header: str):
    # Retrieves all short URL entries from the database.
    if authorization_header not in JWT_Table:
        return None
    
    return list(url_store.values())


def delete_all_short_urls(authorization_header: str):
    # Deletes all short URL entries from the database.
    if authorization_header not in JWT_Table:
        return None

    with lock:
        url_store.clear()
