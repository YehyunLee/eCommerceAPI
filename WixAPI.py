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

    def get_access_token(self) -> str:
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

    def create_product(self, access_token, product_data: dict) -> str:
        """
        :param access_token:
        :param product_data:
        :return: return product id as str
        """
        base_url = 'https://www.wixapis.com/stores/v1/products'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        response = requests.post(base_url, data=json.dumps(product_data), headers=headers)
        product_id = response.json()['product']['id']
        return product_id

    def list_folders(self, access_token: str) -> dict:
        base_url = 'https://www.wixapis.com/site-media/v1/folders'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        response = requests.get(base_url, headers=headers)
        return response.json()

    def import_file(self, access_token, folder_id: str, file_url: str) -> dict:
        base_url = 'https://www.wixapis.com/site-media/v1/files/import'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        data = {
            "url": file_url,
            "parentFolderId": folder_id
        }
        response = json.loads('{}')
        try_num = 0
        while try_num <= 3:
            try:
                try_num += 1
                response = requests.post(base_url, data=json.dumps(data), headers=headers)
                break
            except Exception as e:
                print(e)
        return response.json()  # simplejson.errors.JSONDecodeError: Expecting value: line 1 column 3 (char 2)

    def _query_100_products(self, access_token, offset) -> dict:
        # POST
        base_url = 'https://www.wixapis.com/stores-reader/v1/products/query'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        data = {
            "query": {
                "limit": 100,
                "offset": offset
            },
            "includeVariants": False,
            "includeHiddenProducts": True,
            "includeMerchantSpecificData": False
        }
        response = requests.post(base_url, data=json.dumps(data), headers=headers)
        return response.json()

    def query_all_products(self, access_token) -> dict:
        offset = 0
        products = {}
        past_response = None
        while True:
            response = self._query_100_products(access_token, offset)
            if past_response == response:
                break
            products.update(response)
            offset += 100
            past_response = response
        return products

    def add_product_media(self, access_token, product_id: str, media_data: dict) -> dict:
        base_url = f'https://www.wixapis.com/stores/v1/products/{product_id}/media'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        response = requests.post(base_url, data=json.dumps(media_data), headers=headers)
        return response.json()

    def query_100_collections(self, access_token) -> dict:
        base_url = 'https://www.wixapis.com/stores/v1/collections/query'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        data = {
            "query": {},
            "includeNumberOfProducts": False,
            "includeDescription": False
        }
        response = requests.post(base_url, data=json.dumps(data), headers=headers)
        return response.json()

    def bulk_delete_files(self, access_token, file_ids: list) -> dict:
        base_url = 'https://www.wixapis.com/site-media/v1/bulk/files/delete'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        data = {
            "fileIds": file_ids,
            "permanent": True
        }
        response = requests.post(base_url, data=json.dumps(data), headers=headers)
        return response.json()

    def add_products_to_collection(self, access_token, collection_id: str, product_ids: list[str]) -> dict:
        base_url = f'https://www.wixapis.com/stores/v1/collections/{collection_id}/productIds'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        data = {
            "productIds": product_ids
        }
        response = requests.post(base_url, data=json.dumps(data), headers=headers)
        return response.json()

# Refer to this for id, secret, refresh token
# https://youtu.be/Ocp2vDiPq0A?si=m0G3Geur1pxF87FB
