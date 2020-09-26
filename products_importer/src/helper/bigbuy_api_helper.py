import json

import requests

from products_importer.src import project_config


class BigbuyApiHelper:
    config = project_config.Config()
    headers = {}

    def __init__(self, _config, _headers):
        self.config = _config
        self.headers = _headers

    def request_endpoint(self, endpoint):
        uri = self.config.BIGBUY_API_URI + endpoint
        r = requests.get(url=uri, headers=self.headers)
        print str(r.status_code) + " " + str(r.reason)
        json_data = json.loads(r.text)
        return json_data
