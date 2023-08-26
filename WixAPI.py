import requests
import json


class WixAPI:
    client_id: str
    client_secret: str
    refresh_token: str

    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def get_access_token(self):
        # Set up the OAuth endpoint
        oauth_url = 'https://www.wix.com/oauth/access'

        # Set up the OAuth parameters
        oauth_data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }

        # Obtain an access token
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(oauth_url, data=json.dumps(oauth_data), headers=headers)
        access_token = response.json()['access_token']
        # refresh_token = response.json()['refresh_token']
        return access_token

    def create_product(self, access_token, product_data: dict):
        # Set up the API endpoint
        base_url = 'https://www.wixapis.com/stores/v1/products'

        # Set up the headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        response = requests.post(base_url, data=json.dumps(product_data), headers=headers)
        product_id = response.json()['product']['id']
        return product_id

    def add_media(self, access_token, product_id: str, media_data: dict):
        base_url = f'https://www.wixapis.com/stores/v1/products/{product_id}/media'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        response = requests.post(base_url, data=json.dumps(media_data), headers=headers)
        return response


# Refer to this for id, secret, refresh token
# https://youtu.be/Ocp2vDiPq0A?si=m0G3Geur1pxF87FB
