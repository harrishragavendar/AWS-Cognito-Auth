import requests
import yaml

with open("config.yaml") as file:
    config = yaml.safe_load(file)


def print_post_request(url, body, headers):
    print(f"\tURL: {url}")
    print(f"\tRequest body: {body}")
    print(f"\tHeaders: {headers}")


def register_user(email, name, password):
    headers = {
        "X-Amz-Target": config["cognito_headers"]["signup"],
        "Content-Type": config["cognito_headers"]["content_type"]
    }

    body = {
        "ClientId": config["client_id"],
        "Username": email,
        "Password": password,
        "UserAttributes": [
            {"Name": "email", "Value": email},
            {"Name": "name", "Value": name}
        ]
    }
    url = config["cognito_url"]
    print(f"Making a POST request to register user: {email}")
    print_post_request(url, body, headers)
    user_register_response = requests.post(url, json=body, headers=headers)
    return user_register_response


def verify_user(email, verification_code):
    headers = {
        "X-Amz-Target": config["cognito_headers"]["confirm_signup"],
        "Content-Type": config["cognito_headers"]["content_type"]
    }

    body = {
        "ClientId": config["client_id"],
        "Username": email,
        "ConfirmationCode": verification_code
    }
    url = config["cognito_url"]
    print(f"Making a POST request to verify user: {email}")
    print_post_request(url, body, headers)
    user_verification_response = requests.post(url, json=body, headers=headers)
    return user_verification_response


def authenticate_user(email, password):
    headers = {
        "X-Amz-Target": config["cognito_headers"]["initiate-auth"],
        "Content-Type": config["cognito_headers"]["content_type"]
    }

    body = {
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": config["client_id"],
        "AuthParameters": {
            "USERNAME": email,
            "PASSWORD": password
        }
    }
    url = config["cognito_url"]
    print(f"Making a POST request to authenticate user: {email}")
    print_post_request(url, body, headers)
    auth_response = requests.post(url=url, json=body, headers=headers)
    return auth_response


def access_resource(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(config["resource_url_1"], headers=headers)
    return response
