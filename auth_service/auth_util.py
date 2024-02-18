import requests
import json
import base64
import hashlib
import hmac


def notify_url_service(jwt_token, username):
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
    generate a JWT token with the header and payload
    header is a list
    payload is a dictionary
    """

    encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    secret_key = 'wscs_is_very_nice'
    signature = hmac.new(secret_key.encode(), f"{encoded_header}.{encoded_payload}".encode(), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode()

    jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    return jwt_token