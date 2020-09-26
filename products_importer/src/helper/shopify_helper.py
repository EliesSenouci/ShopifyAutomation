import json

import requests

from products_importer.src import project_config


class ShopifyHelper:
    config = project_config.Config()

    def __init__(self, _config):
        self.config = _config

    def get_store_uri(self, endpoint):
        uri = "https://" + self.config.SHOPIFY_API_KEY + ":" + self.config.SHOPIFY_API_PASSWORD + "@" + \
              self.config.STORE_NAME + "/" + endpoint
        return uri

    def send_get_request_to_store_api(self, endpoint, params=None):
        if params is None:
            params = {}
        uri = self.get_store_uri(endpoint)
        headers = {"Content-Type": "application/json"}
        print "Send request to " + uri
        r = requests.get(url=uri, headers=headers, params=params)
        json_data = json.loads(r.text)
        return json_data
