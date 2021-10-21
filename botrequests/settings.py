import requests

from config import url_locale, headers


def get_list_locale():
    return requests.request("GET", url_locale, headers=headers).json()