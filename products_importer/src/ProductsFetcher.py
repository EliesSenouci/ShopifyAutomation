from Product import Product
from products_importer.src import project_config
from products_importer.src.helper import bigbuy_api_helper


class ProductsFetcher:
    config = project_config.Config()
    bigbuy_api_helper = bigbuy_api_helper.BigbuyApiHelper
    HEADERS = {
        "Accept": "text/plain",
        "Content-type": "application/json",
    }

    def __init__(self, _config):
        self.config = _config
        self.HEADERS["Authorization"] = "Bearer " + self.config.BIGBUY_API_KEY
        self.bigbuy_api_helper = bigbuy_api_helper.BigbuyApiHelper(_config, self.HEADERS)

    def get_product_categories(self):
        categories = []
        json_data = self.bigbuy_api_helper.request_endpoint("/rest/catalog/productscategories.json?isoCode=fr")
        for category in json_data:
            if int(category["category"]) in self.config.CATEGORIES:
                categories.append(category)
        return categories

    def get_products_images(self):
        print "Fetch all products images"
        images = []
        json_data = self.bigbuy_api_helper.request_endpoint("/rest/catalog/productsimages.json?isoCode=fr")
        for data in json_data:
            images_list = []
            for i in data["images"]:
                entry = {
                    "src": i["url"]
                }
                images_list.append(entry)
            image = {
                "product_id": data["id"],
                "images": images_list
            }
            images.append(image)
        return images

    def get_products_infos(self):
        print "Fetch all products informations"
        products_infos = []
        json_data = self.bigbuy_api_helper.request_endpoint("/rest/catalog/products.json?isoCode=fr")
        for data in json_data:
            if data["category"] in self.config.CATEGORIES:
                product_info = {
                    "attributes": data["attributes"],
                    "product_type_id": data["category"],
                    "product_id": data["id"],
                    "price": data["retailPrice"],
                    "sku": data["sku"],
                    "barcode": data["ean13"],
                    "weight": data["weight"],
                    "height": data["height"],
                    "width": data["width"],
                    "metafields": [
                        {
                            "key": "bigbuy_id",
                            "value": data["id"],
                            "value_type": "integer",
                            "namespace": "global"
                        }
                    ]
                }
                products_infos.append(product_info)
        return products_infos

    def get_variant_name(self):
        json_data = self.bigbuy_api_helper.request_endpoint("/rest/catalog/variations.json")
        return json_data

    def format_bigbuy_products(self, products, products_categories):
        print "Format products to BigBuy format"
        formatted_products = []
        all_product_images = self.get_products_images()
        products_infos = self.get_products_infos()
        for item in products:
            product = Product(item, products_infos, all_product_images, products_categories)
            if product.is_valid_product:
                formatted_products.append(product.to_json())
                print "Product added " + str(product.to_json())
        return formatted_products

    def get_desired_products_categories(self):
        print "Fetch all categories"
        json_data = self.bigbuy_api_helper.request_endpoint("/rest/catalog/categories.json?isoCode=fr")
        categories = []
        for category in json_data:
            if category["id"] in self.config.CATEGORIES:
                categories.append(category)
        return categories

    def keep_products_of_desired_categories(self, all_products):
        print "Sorting of categories"
        products = []
        categories = self.get_product_categories()
        for product in all_products:
            for category in categories:
                if int(category["product"]) == int(product["id"]):
                    products.append(product)
                    break
        return products

    def get_all_products(self):
        print "Fetch all products from API"
        json_data = self.bigbuy_api_helper.request_endpoint("/rest/catalog/productsinformation.json?isoCode=fr")
        return json_data

    @staticmethod
    def get_attributes_names_by_id(attribute_ids, attributes_names):
        names = []
        for attribute_name in attributes_names:
            for attribute_id in attribute_ids:
                if attribute_id["id"] == attribute_name["id"]:
                    names.append(attribute_name["name"])
        return names

    def add_attributes_to_variants(self, product_variant, attributes_per_variants, attributes_names):
        for variant_attributes in attributes_per_variants:
            if variant_attributes["id"] == product_variant["id"]:
                names = self.get_attributes_names_by_id(variant_attributes["attributes"], attributes_names)
                product_variant["attributes"] = names
        return product_variant

    @staticmethod
    def get_products_variants(variants_per_products, p):
        products_variants = []
        for v in variants_per_products:
            if v["product"] == p["id"]:
                products_variants.append(v)
        return products_variants

    @staticmethod
    def get_variant_attributes(variant, attributes_per_variants):
        for attribut in attributes_per_variants:
            if variant["id"] == attribut["id"]:
                return attribut["attributes"]

    @staticmethod
    def get_attribut_info(attribut_id, attributes_names):
        for info in attributes_names:
            if info["id"] == attribut_id:
                return info
        return None

    @staticmethod
    def get_attribute_group_name(att_info, attributes_group):
        for group in attributes_group:
            if att_info["attributeGroup"] == group["id"]:
                return group["name"]

    @staticmethod
    def group_exist_in_options(options, group_name):
        for o in options:
            if o["name"] == group_name:
                return True
        return False

    @staticmethod
    def attribute_exist_in_option(options, group_name, attribute_name):
        for o in options:
            if o["name"] == group_name:
                for a in o["values"]:
                    if a == attribute_name:
                        return True
        return False

    @staticmethod
    def add_attribute_in_option(options, group_name, attribute_name):
        for o in options:
            if o["name"] == group_name:
                o["values"].append(attribute_name)
        return options

    def fill_options(self, options, group_name, attribute_name):
        if self.group_exist_in_options(options, group_name):
            if self.attribute_exist_in_option(options, group_name, attribute_name):
                return
            else:
                options = self.add_attribute_in_option(options, group_name, attribute_name)
        else:
            options.append({
                "name": group_name,
                "values": [
                    attribute_name
                ]
            })
        return options

    @staticmethod
    def fill_variants(variant, att_info, group_name, options, variants):
        v = {}
        options_values = []
        for o in options:
            if o["name"] == group_name:
                options_values.append(att_info["name"])
        i = 1
        for o in options_values:
            v["option" + str(i)] = o
            i = i + 1
        v["price"] = variant["retailPrice"]
        v["sku"] = variant["sku"]
        v["barcode"] = variant["ean13"]
        v["weight"] = variant["extraWeight"]
        v["weight_unit"] = "kg"
        variants.append(v)
        return variants

    def get_options(self, product_variants, attributes_group, attributes_names, attributes_per_variants):
        options = []
        variants = []
        for variant in product_variants:
            variant_attributes_ids = self.get_variant_attributes(variant, attributes_per_variants)
            for attribut_id in variant_attributes_ids:
                att_info = self.get_attribut_info(attribut_id["id"], attributes_names)
                group_name = self.get_attribute_group_name(att_info, attributes_group)
                options = self.fill_options(options, group_name, att_info["name"])
                variants = self.fill_variants(variant, att_info, group_name, options, variants)
        return variants, options

    def get_products_variations(self, desired_products):
        variants_per_products = self.bigbuy_api_helper.request_endpoint("/rest/catalog/productsvariations.json?isoCode=fr")
        attributes_per_variants = self.bigbuy_api_helper.request_endpoint("/rest/catalog/variations.json")
        attributes_names = self.bigbuy_api_helper.request_endpoint("/rest/catalog/attributes.json?isoCode=fr&_format=json")
        products_with_variations = []
        attributes_groups = self.bigbuy_api_helper.request_endpoint("/rest/catalog/attributegroups.json?isoCode=fr&_format=json")
        for product in desired_products:
            p = product
            product_variants = self.get_products_variants(variants_per_products, p)
            variants, options = self.get_options(product_variants, attributes_groups, attributes_names,
                                                 attributes_per_variants)
            if not variants:
                variants = {}
            p["variants"] = variants
            p["options"] = options
            products_with_variations.append(p)
        return products_with_variations

    def process(self):
        print "Starting to fetch products on " + self.config.BIGBUY_API_URI
        all_products = self.get_all_products()
        products_categories = self.get_desired_products_categories()
        desired_products = self.keep_products_of_desired_categories(all_products)
        desired_products = self.get_products_variations(desired_products)
        formatted_products = self.format_bigbuy_products(desired_products, products_categories)
        print (str(len(formatted_products)) + " products fetched.")
        return formatted_products
