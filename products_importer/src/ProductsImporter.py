import json

import requests

from products_importer.src import project_config
from products_importer.src.helper import shopify_helper


class ProductsImporter:
    config = project_config.Config()
    shopify_helper = shopify_helper.ShopifyHelper

    def __init__(self, _config):
        self.config = _config
        self.shopify_helper = shopify_helper.ShopifyHelper(_config)

    def process(self, products):
        uri = self.shopify_helper.get_store_uri("/admin/products.json")
        headers = {"Content-Type": "application/json"}
        for product in products:
            data = {"product": product}
            r = requests.post(url=uri, data=json.dumps(data), headers=headers)
            print r
