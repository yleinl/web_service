from utils import generate_short_id

url_store = {}


def create_short_url(url: str):
    """
    Checks if a short URL ID for the given long URL already exists. If not,
    generates a new short ID and creates a new short URL entry in the memory.

    :param url: The given URL to be shortened.
    :return: The existing or newly created short URL object.
    """
    global url_store
    for short_id, url_info in url_store.items():
        if url_info['long_url'] == url:
            return url_info
    attempt = 0
    length = 8
    while True:
        url_id = generate_short_id(url, length, attempt)
        if url_id not in url_store:
            url_store[url_id] = {'id': url_id, 'long_url': url}
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


def update_long_url_by_id(url_id: str, new_url: str):
    """
    Updates the long URL of an existing id in the database.

    :param url_id: The URL ID to update.
    :param new_url: The new long URL to associate with the short URL.
    :return: The updated short URL object if successful, else None.
    """
    if url_id in url_store:
        url_store[url_id]['long_url'] = new_url
        return url_store[url_id]
    else:
        return None


def delete_short_url(url_id: str):
    """
    Deletes a short URL entry from the database by its URL ID.
    :param url_id: The URL ID of the short URL to delete.
    :return: True if deletion was successful, else False (URL ID not found).
    """
    if url_id in url_store:
        del url_store[url_id]
        return True
    else:
        return False


def get_all_short_urls():
    # Retrieves all short URL entries from the database.
    return list(url_store.values())


def delete_all_short_urls():
    # Deletes all short URL entries from the database.
    url_store.clear()
