import time

import requests
import json
import base64
import hashlib
import hmac


def notify_url_service(jwt_token, username):
    """
    Notify the url shorten service with a JWT token and username for authentication.
    :param jwt_token: The JWT token to send.
    :param username: The username associated with the JWT token.
    """
    business_service_url = "http://127.0.0.1:5000/authorization"
    payload = {'jwt': jwt_token, 'username': username}
    response = requests.post(business_service_url, json=payload)
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print("Failed to send notification")


"""
generate a JWT token with the header and payload
"""


def JWT_generate(header, payload):
    """
    Generate a JWT token with the provided header and payload.
    :param header: A list containing the header information.
    :param payload: A dictionary containing the payload information.
    :return: The generated JWT token.
    """
    payload['exp'] = int(time.time()) + 3600
    encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    secret_key = 'wscs_is_very_nice'
    signature = hmac.new(secret_key.encode(), f"{encoded_header}.{encoded_payload}".encode(), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode()

    jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    return jwt_token
