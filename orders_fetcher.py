import requests
import json

API_KEY = ""
API_PASSWORD = ""
STORE_NAME = ""


def get_store_uri():
    uri = "https://" + API_KEY + ":" + API_PASSWORD + "@" + STORE_NAME + "/"
    return uri


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


def format_products(data):
    products = []
    for line in data["line_items"]:
        product = {
            "reference": line["id"],
            "quantity": line["fulfillable_quantity"]
        }
        products.append(product)
    return products


def format_carriers(data):
    return None


def format_orders(r):
    orders = []
    json_data = json.loads(r.text)
    for data in json_data["orders"]:
        products = format_products(data)
        carriers = format_carriers()
        shipping_address = format_shipping_address(data)
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


def get_all_orders():
    uri = get_store_uri()
    uri += "/admin/orders.json"
    r = requests.get(url=uri)
    orders = format_orders(r)
    return orders


def main():
    orders = get_all_orders()
    print "Done"


if __name__ == '__main__':
    main()
