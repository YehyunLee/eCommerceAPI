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
        oauth_url = 'https://www.wix.com/oauth/access'

        oauth_data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(oauth_url, data=json.dumps(oauth_data), headers=headers)
        access_token = response.json()['access_token']
        # refresh_token = response.json()['refresh_token']
        return access_token

    def create_product(self, access_token, product_data: dict):
        base_url = 'https://www.wixapis.com/stores/v1/products'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        response = requests.post(base_url, data=json.dumps(product_data), headers=headers)
        product_id = response.json()['product']['id']
        return product_id

# 1. create folders
# 2. https://dev.wix.com/docs/rest/api-reference/media/media-manager/files/import-file     uploade file
# 3. add media

    # POST list of folder id with access token as parameter

    def get_folder_id(self, access_token: str):
        base_url = 'https://www.wixapis.com/site-media/v1/folders/search'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        body = {
            'rootFolder': 'MEDIA_ROOT',
            'sort': {
                'fieldName': 'displayName',
                'order': 'ASC'
            },
            'paging': {
                'limit': 20
            }
        }

        response = requests.post(base_url, data=json.dumps(body), headers=headers)

        folders = response.json()['folders']

        return folders[0]['id'] if folders else None


    def upload_file(self, file_url: str, parent_folder_id: str, access_token: str):
        base_url = 'https://www.wixapis.com/site-media/v1/files/generate-upload-url'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        body = {
            'mimeType': '*/*',
            'fileName': None,
            'parentFolderId': parent_folder_id
        }

        response = requests.post(base_url, data=json.dumps(body), headers=headers)
        upload_url = response.json()['uploadUrl']

        file_content = requests.get(file_url).content

        response = requests.put(upload_url, data=file_content)

        media_id = response.json()['mediaId']

        return media_id

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
