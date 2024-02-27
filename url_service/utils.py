import base64
import json
import string
import re
import time


BASE62 = string.digits + string.ascii_letters

JWT_Table = {}


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


def hash_encoder(url):
    """
    Hash the url to uniform it

    :param url: The url to be hashed.
    :return: The hash value of the url String
    """
    url = str(url)
    hash_value = 0
    for char in url:
        hash_value = (hash_value * 31 + ord(char)) % 2 ** 64
    return hash_value


def generate_short_id(url, length=5, attempt=0):
    """
    Generates a unique short ID for a given URL.

    :param url: Original URL to be shortened.
    :param length: Desired length of the short ID.
    :param attempt: Current attempt number to handle collision.
    :return: A short ID based on the URL.
    """
    unique_input = url + str(attempt)
    decimal = hash_encoder(unique_input.encode('utf-8'))
    short_id = base62_encode(decimal)[:length]
    return short_id


def is_valid_url(url):
    """
    Validate the url format

    :param url: a given to be shortened.
    :return: validation result True or False
    """
    regex = re.compile(
        r'(https?://[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}(?::\d+)?'
        r'|\b[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}(?::\d+)?'
        r'|localhost(?::\d+)?'
        r'|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?)', re.IGNORECASE)
    return re.match(regex, url) is not None


def parse_jwt(token):
    header, payload, signature = token.split('.')
    decoded_payload = base64.urlsafe_b64decode(payload + '==').decode('utf-8')
    return json.loads(decoded_payload)


def is_jwt_expired(token):
    payload = parse_jwt(token)
    exp = payload.get('exp')

    if exp is not None:
        if int(exp) < time.time():
            return True
    return False



def verify_jwt(jwt_token, secret_key):
    """
    Verify the validity of a JWT token.
    :param jwt_token: The JWT token to verify.
    :param secret_key: The secret key used for signing the JWT token.
    :return: True if the JWT token is valid, False otherwise.
    """
    try:
        encoded_header, encoded_payload, encoded_signature = jwt_token.split('.')

        # Decode header and payload
        header = json.loads(base64.urlsafe_b64decode(encoded_header.encode()).decode())
        payload = json.loads(base64.urlsafe_b64decode(encoded_payload.encode()).decode())

        # Recalculate signature
        signature = hmac.new(secret_key.encode(), f"{encoded_header}.{encoded_payload}".encode(),
                             hashlib.sha256).digest()
        recalculated_signature = base64.urlsafe_b64encode(signature).decode()

        # Compare signatures
        if recalculated_signature == encoded_signature:
            # Check expiration time
            current_time = int(time.time())
            if 'exp' in payload and payload['exp'] >= current_time:
                return True
    except Exception as e:
        print("Error verifying JWT:", str(e))

    return False