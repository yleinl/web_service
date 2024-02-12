import hashlib
import string
import re
BASE62 = string.digits + string.ascii_letters


def base62_encode(num):
    """
    Encodes a given integer into a base62 string. Base62 is chosen for URL shortening
    because it's more compact than decimal and is URL-safe.

    :param num: The integer to be encoded.
    :return: A base62 encoded string.
    """
    if num == 0:
        return BASE62[0]
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62[rem])
    return ''.join(reversed(base62))


def generate_short_id(url, length=8, attempt=0):
    """
    Generates a unique short ID for a given URL.

    :param url: Original URL to be shortened.
    :param length: Desired length of the short ID.
    :param attempt: Current attempt number to handle collision.
    :return: A short ID based on the URL.
    """
    unique_input = url + str(attempt)
    hash_obj = hashlib.sha256(unique_input.encode('utf-8'))
    decimal = int(hash_obj.hexdigest(), 16)
    short_id = base62_encode(decimal)[:length]
    return short_id


def is_valid_url(url):
    """
    Validate the url format

    :param url: a given to be shortened.
    :return: validation result True or False
    """
    regex = re.compile(
        r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}(?::\d+)?'
        r'|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}(?::\d+)?'
        r'|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}(?::\d+)?'
        r'|www\.[a-zA-Z0-9]+\.[^\s]{2,}(?::\d+)?'
        r'|localhost(?::\d+)?'
        r'|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?'
        r')', re.IGNORECASE)
    return re.match(regex, url) is not None