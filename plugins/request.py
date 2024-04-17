from data_singleton.base import BasePlugin
from flask import request

class RequestPlugin(BasePlugin):
    def get_request_data(self, key, default=None):
        return request.form.get(key, default)

    def get_request_headers(self, key, default=None):
        return request.headers.get(key, default)