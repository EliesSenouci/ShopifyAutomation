import json

import requests

from products_importer.src import project_config
from products_importer.src.helper import shopify_helper


class OrdersFetcher(object):
    config = project_config.Config()
    shopify_helper = shopify_helper.ShopifyHelper

    def __init__(self, _config):
        self.config = _config
        self.shopify_helper = shopify_helper.ShopifyHelper(_config)

    def get_store_uri(self):
        uri = "https://" + self.config.SHOPIFY_API_KEY + ":" + self.config.SHOPIFY_API_PASSWORD + "@" + self.config.STORE_NAME + "/"
        return uri

    @staticmethod
    def format_shipping_address(data):
        shipping_address = {
           "firstName": data["shipping_address"]["first_name"],
           "lastName": data["shipping_address"]["last_name"],
           "country": data["shipping_address"]["country_code"],
           "postcode": data["shipping_address"]["zip"],
           "town": data["shipping_address"]["city"],
           "address": data["shipping_address"]["address1"],
           "phone": data["shipping_address"]["phone"],
           "email": data["email"],
           "comment": ""
        }
        return shipping_address

    @staticmethod
    def format_products(data):
        products = []
        for line in data["line_items"]:
            product = {
                "reference": line["id"],
                "quantity": line["fulfillable_quantity"]
            }
            products.append(product)
        return products

    @staticmethod
    def format_carriers(data):
        return None

    def format_orders(self, r):
        orders = []
        json_data = json.loads(r.text)
        for data in json_data["orders"]:
            products = self.format_products(data)
            carriers = self.format_carriers(data)
            shipping_address = self.format_shipping_address(data)
            order = {
                "internal_reference": "",
                "language": data["shipping_address"]["country_code"],
                "paymentMethod": "",
                "carriers": carriers,
                "shippingAddress": shipping_address,
                "products": products
            }
            orders.append(order)
        return orders

    def get_all_orders(self):
        uri = self.get_store_uri()
        uri += "/admin/orders.json"
        r = requests.get(url=uri)
        orders = self.format_orders(r)
        return orders

    def process(self):
        orders = self.get_all_orders()
        print orders
