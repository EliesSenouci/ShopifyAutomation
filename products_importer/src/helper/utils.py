from bigbuy_products_fetcher import *


def write_products_in_file():
    print "Fetch all categories"
    json_data = request_endpoint("/rest/catalog/categories.json?isoCode=fr")
    f = open("categories.txt", "w")
    for category in json_data:
        f.write(str(category))
        f.write("\n\n")

