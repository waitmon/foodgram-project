import requests


class BasicHttpMethods:
    """Basic HTTP Methods for API testing process: get, post, put, patch, delete."""

    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'
               }

    cookies = ''

    @staticmethod
    def get(url):
        response = requests.get(url, headers=BasicHttpMethods.headers)
        return response

    @staticmethod
    def post_no_token(url, body):
        response = requests.post(url, json=body, headers=BasicHttpMethods.headers)
        return response

    @staticmethod
    def put(url, body, cookies):
        response = requests.put(url, json=body, headers=BasicHttpMethods.headers, cookies=cookies)
        return response

    @staticmethod
    def patch(url, body, cookies):
        response = requests.patch(url, json=body, headers=BasicHttpMethods.headers, cookies=cookies)
        return response

    @staticmethod
    def delete(url):
        response = requests.delete(url, headers=BasicHttpMethods.headers)
        return response
