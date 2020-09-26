class Config:
    NAME = ""
    SHOPIFY_API_KEY = ""
    SHOPIFY_API_PASSWORD = ""
    STORE_NAME = ""
    BIGBUY_API_KEY = ""
    BIGBUY_API_PASSWORD = ""
    BIGBUY_API_URI = ""
    CATEGORIES = [2660, 2627, 3021, 2904, 2946, 2759, 2628, 2583, 2576, 2578, 2913, 2585, 2574, 2581, 2579, 2589, 2587]


class DevelopmentConfig(Config):
    NAME = "development"
    SHOPIFY_API_KEY = ""
    SHOPIFY_API_PASSWORD = ""
    STORE_NAME = ""
    BIGBUY_API_KEY = ""
    BIGBUY_API_PASSWORD = ""
    BIGBUY_API_URI = ""


class ProductionConfig(Config):
    NAME = "production"
    SHOPIFY_API_KEY = ""
    SHOPIFY_API_PASSWORD = ""
    STORE_NAME = ""
    BIGBUY_API_KEY = ""
    BIGBUY_API_PASSWORD = ""
    BIGBUY_API_URI = ""
