from products_importer.src import ProductsFilter, ProductsImporter, ProductsFetcher, project_config, OrdersFetcher


def main(_config):
    # print "Start in " + _config.NAME + " mode"
    # product_fetcher = ProductsFetcher.ProductsFetcher(_config)
    # products = product_fetcher.process()
    #
    # print ("Start filtering...")
    # products_filter = ProductsFilter.ProductsFilter(_config)
    # new_products = products_filter.process(products)
    #
    # print ("Ready to import " + str(len(new_products)) + " new products " + "on " + str(len(products)) + " products")
    # products_importer = ProductsImporter.ProductsImporter(_config)
    # products_importer.process(new_products)

    print ("Ready to fetch costumers orders")
    orders_fetcher = OrdersFetcher.OrdersFetcher(_config)
    orders_fetcher.process()


if __name__ == '__main__':
    profile = "prod"
    config = project_config.Config()
    if profile == "dev":
        config = project_config.DevelopmentConfig()
    elif profile == "prod":
        config = project_config.ProductionConfig()
    else:
        print "Error : No profile founded"
        exit(1)
    main(config)
