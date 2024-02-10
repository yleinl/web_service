import models
from utils import generate_short_id


url_store = {}


def create_short_url(url: str):
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
        attempt += 1


def get_short_url_by_id(urlid: str):
    return url_store.get(urlid, None)


def update_long_url_by_id(url_id: str, new_url: str):
    if url_id in url_store:
        url_store[url_id]['long_url'] = new_url
        return url_store[url_id]
    else:
        return None


def delete_short_url(url_id: str):
    if url_id in url_store:
        del url_store[url_id]
        return True
    else:
        return False


def get_all_short_urls():
    return list(url_store.values())


def delete_all_short_urls():
    url_store.clear()
    return True