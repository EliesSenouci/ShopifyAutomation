import json

import requests

API_KEY = ""
API_PASSWORD = ""
URI = "https://api.sandbox.bigbuy.eu"


def list_categories():
    uri = URI + "/rest/catalog/categories.json?isoCode=fr"
    headers = {
        "Accept": "text/plain",
        "Content-type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }
    r = requests.get(url=uri, headers=headers)
    return r


def list_categories_product(category_id):
    uri = URI + "/rest/catalog/productscategories.json?isoCode=fr"
    headers = {
        "Accept": "text/plain",
        "Content-type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }
    r = requests.get(url=uri, headers=headers)
    return r


def init_order():
    order = {
        "internalReference": "123456",
        "language": "es",
        "paymentMethod": "moneybox",
        "carriers": [
            {
                "name": "correos"
            },
            {
                "name": "chrono"
            }
        ],
        "shippingAddress": {
            "firstName": "John",
            "lastName": "Doe",
            "country": "ES",
            "postcode": "46005",
            "town": "Valencia",
            "address": "C/ Altea",
            "phone": "664869570",
            "email": "john@email.com",
            "comment": ""
        },
        "products": [
            {
                "reference": "V0100100",
                "quantity": 1
            },
            {
                "reference": "F1505138",
                "quantity": 4
            }
        ]
    }


def main():
    print "Done"


if __name__ == '__main__':
    main()
