class Product:
    def __init__(self, item, products_infos, all_product_images, products_categories):
        product_info = self.get_product_infos_by_id(item["id"], products_infos)
        if product_info is not None:
            self.set_title(item)
            self.set_body_html(item)
            self.set_height(product_info)
            self.set_images(item, all_product_images)
            self.set_metafields(product_info)
            self.set_product_type(product_info, products_categories)
            self.set_vendor()
            self.set_width(product_info)
            self.set_variants(item, product_info)
            self.is_valid_product = True

    height = 0
    width = 0
    variants = []
    options = []
    title = ""
    body_html = ""
    vendor = ""
    product_type = ""
    images = ""
    metafields = ""
    is_valid_product = False

    def set_height(self, product_info):
        self.height = product_info["height"]

    def set_width(self, product_info):
        self.width = product_info["width"]

    def get_attribute_by_id(self, variants_names):
        pass

    @staticmethod
    def get_first(iterable, default=None):
        if iterable:
            for item in iterable:
                return item
        return default

    def add_variants(self, variations):
        i = 1
        for v in variations:
            v["price"] = v.pop("retailPrice")
            v["option" + str(i)] = self.get_first(v["attributes"])
        return variations

    def set_variants(self, item, product_info):
        if len(item["options"]) != 0:
            self.options = item["options"]
            self.variants = item["variants"]
        else:
            self.variants = [{
                "title": "Standard",
                "sku": item["sku"],
                "barcode": product_info["barcode"],
                "price": product_info["price"],
                "weight": product_info["weight"],
                "weight_unit": "kg",
            }]

    def set_title(self, item):
        self.title = item["name"]

    def set_body_html(self, item):
        self.body_html = item["description"]

    def set_vendor(self):
        self.vendor = "BigBuy"

    @staticmethod
    def get_category_name_by_id(category_id, products_categories):
        for category in products_categories:
            if category["id"] == category_id:
                return category["name"]
        return None

    def set_product_type(self, product_info, products_categories):
        pt = self.get_category_name_by_id(product_info["product_type_id"], products_categories)
        self.product_type = pt

    @staticmethod
    def get_product_image(product_id, all_products_images):
        for product_image in all_products_images:
            if product_image["product_id"] == product_id:
                return product_image["images"]
        return None

    def set_images(self, item, all_product_images):
        self.images = self.get_product_image(item["id"], all_product_images)

    def set_metafields(self, product_info):
        self.metafields = product_info["metafields"]

    @staticmethod
    def get_product_infos_by_id(product_id, products_infos):
        for infos in products_infos:
            if infos["product_id"] == product_id:
                return infos
        return None

    def to_json(self):
        json = {
            "title": self.title,
            "body_html": self.body_html,
            "height": self.height,
            "width": self.width,
            "images": self.images,
            "metafields": self.metafields,
            "product_type": self.product_type,
            "vendor": self.vendor,
            "variants": self.variants,
            "options": self.options
        }
        return json
