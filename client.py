from urllib import parse

import requests

class ApiClient:
    def __init__(self, api_key, base_url="https://cockpit.shirtigo.de/api/"):
        # store base url, resource url will be appended
        self.base_url = base_url

        # initialize requests Session in order to share headers/cookies between requests
        self.session = requests.Session()

        # set OAuth/Authorization header
        self.session.headers.update({
            "User-Agent": "Shirtigo Cockpit Python REST API Client",
            "Authorization": "Bearer " + api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def _request(self, url, method="GET", data=None, params=None):
        url = parse.urljoin(self.base_url, url)

        # issue request
        response = self.session.request(method, url, json=data, params=params)
        response_data = response.json()
        
        if not response.ok:
            # extract error and throw Python exception
            raise RuntimeError(response_data["message"])

        return response_data

    def get(self, url, params=None):
        return self._request(url, "GET", None, params)

    def post(self, url, data=None, params=None):
        return self._request(url, "POST", data, params)

    def put(self, url, data=None, params=None):
        return self._request(url, "PUT", data, params)

    def delete(self, url, params=None):
        return self._request(url, "DELETE", None, params)
