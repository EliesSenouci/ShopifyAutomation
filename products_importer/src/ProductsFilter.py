from products_importer.src import project_config
from products_importer.src.helper import shopify_helper


class ProductsFilter:
    config = project_config.Config()
    shopify_helper = shopify_helper.ShopifyHelper

    def __init__(self, _config):
        self.config = _config
        self.shopify_helper = shopify_helper.ShopifyHelper(_config)

    def process(self, products):
        return self.filter_existing_products(products)

    def filter_existing_products(self, products):
        new_products = []
        store_products_ids = self.get_store_products_ids()
        bigbuy_existing_products_ids = self.get_bigbuy_existing_ids(store_products_ids)
        for product in products:
            for metafield in product["metafields"]:
                if metafield["key"] == "bigbuy_id":
                    if metafield["value"] not in bigbuy_existing_products_ids:
                        new_products.append(product)
        return new_products

    def get_store_products_ids(self):
        ids = []
        i = 1
        while True:
            params = {
                "limit": 50,
                "page": i,
                "fields": "id"
            }
            json_data = self.shopify_helper.send_get_request_to_store_api("/admin/products.json", params)
            for data in json_data['products']:
                ids.append(data["id"])
            i += 1
            if len(json_data["products"]) < 50:
                break
        return ids

    def get_product_metafields(self, _id):
        json_data = self.shopify_helper.send_get_request_to_store_api("/admin/products/" + str(_id) +
                                                                      "/metafields.json")
        return json_data

    def get_bigbuy_existing_ids(self, store_products_ids):
        bigbuy_existing_products_ids = []
        for store_product_id in store_products_ids:
            product_metafields = self.get_product_metafields(store_product_id)
            for metafield in product_metafields["metafields"]:
                if metafield["key"] == "bigbuy_id":
                    bigbuy_existing_products_ids.append(metafield["value"])
        return bigbuy_existing_products_ids
