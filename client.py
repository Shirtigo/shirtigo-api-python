from urllib import parse
import warnings

import requests

class ApiClient:
    def __init__(self, api_key, base_url="https://cockpit.shirtigo.de/api/", ignore_certificates=False):
        # store base url, resource url will be appended
        self.base_url = base_url

        # warn on very short api key
        if len(api_key) < 100:
            warnings.warn("The provided API token appears to be shorter than expected.")

        # initialize requests Session in order to share headers/cookies between requests
        self.session = requests.Session()

        # set OAuth/Authorization header
        self.session.headers.update({
            "User-Agent": "Shirtigo Cockpit Python REST API Client",
            "Authorization": "Bearer " + str(api_key),
            "Accept": "application/json"
        })

        if ignore_certificates:
            # disable SSL certificate validation
            self.session.verify = False

    def _request(self, url, method="GET", data=None, params=None, files=None):
        # construct full URL
        url = parse.urljoin(self.base_url, url)

        headers = {}
        if not files:
            # don't send a json header if the request contains files
            # as a multipart-formdata value will be generated by requests
            headers["Content-Type"] = "application/json"

        # issue request
        response = self.session.request(method, url, json=data, params=params, files=files, headers=headers)

        if response.status_code == 204:
            # 204 = No Content (expected)
            return None

        response_data = response.json()
        if not response.ok:
            # extract error and throw Python exception
            if response.status_code == 401:
                if response.request.url != url:
                    raise RuntimeError("Authentication error. Make sure that the client base url exactly matches the documentation.")
                else:
                    raise RuntimeError("Authentication error. Check whether the provided API key is valid.")
            elif response.status_code == 403 and "required_scopes" in response_data:
                raise RuntimeError("Authorization error. API token requires the following scope(s): %s" % ", ".join(response_data["required_scopes"]))
            elif response.status_code == 422 and "errors" in response_data :
                raise ValueError("Input validation failed: %r" % response_data["errors"])
            elif "message" in response_data:
                raise RuntimeError("Endpoint returned HTTP status %d: %s" %
                    (response.status_code, response_data["message"]))
            else:
                raise RuntimeError("Endpoint returned unhandled HTTP status %d", response.status_code)

        return response_data

    def get(self, url, params=None):
        return self._request(url, "GET", None, params)

    def post(self, url, data=None, params=None, files=None):
        return self._request(url, "POST", data, params, files)

    def put(self, url, data=None, params=None, files=None):
        return self._request(url, "PUT", data, params, files)

    def delete(self, url, params=None):
        return self._request(url, "DELETE", None, params)
