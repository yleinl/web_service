from utils import generate_short_id
import threading

url_store = {}

lock = threading.Lock()


def create_short_url(url: str, user_ip: str):
    """
    Checks if a short URL ID for the given long URL already exists. If not,
    generates a new short ID and creates a new short URL entry in the memory.

    :param user_ip: The user IP address for authorization
    :param url: The given URL to be shortened.
    :return: The existing or newly created short URL object.
    """
    global url_store
    for short_id, url_info in url_store.items():
        if url_info['long_url'] == url:
            return url_info
    attempt = 0
    length = 8
    with lock:
        while True:
            url_id = generate_short_id(url, length, attempt)
            if url_id not in url_store:
                url_store[url_id] = {'id': url_id, 'long_url': url, 'user_ip': user_ip}
                return url_store[url_id]
            # concatenate a different number to handle collision
            attempt += 1


def get_short_url_by_id(urlid: str):
    """
    Retrieves a short URL object by its URL ID.
    :param urlid: The URL ID of the short URL.
    :return: The short URL object if found, else None.
    """
    return url_store.get(urlid, None)


def update_long_url_by_id(url_id: str, new_url: str, user_ip: str):
    """
    Updates the long URL of an existing id in the database.

    :param user_ip: The user IP address for authorization
    :param url_id: The URL ID to update.
    :param new_url: The new long URL to associate with the short URL.
    :return: The updated short URL object if successful, else None.
    """
    if url_id in url_store:
        if url_store[url_id]['user_ip'] != user_ip:
            return None
        with lock:
            url_store[url_id]['long_url'] = new_url
        return url_store[url_id]
    else:
        return None


def delete_short_url(url_id: str, user_ip: str):
    """
    Deletes a short URL entry from the database by its URL ID.
    :param user_ip: The user IP address for authorization
    :param url_id: The URL ID of the short URL to delete.
    :return: True if deletion was successful, else False (URL ID not found).
    """
    if url_id in url_store:
        if url_store[url_id]['user_ip'] != user_ip:
            return None
        with lock:
            del url_store[url_id]
        return True
    else:
        return False


def get_all_short_urls():
    # Retrieves all short URL entries from the database.
    return list(url_store.values())


def delete_all_short_urls():
    # Deletes all short URL entries from the database.
    with lock:
        url_store.clear()
