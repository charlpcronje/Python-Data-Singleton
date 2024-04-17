from data_singleton.base import BasePlugin
import requests
import os

class APIPlugin(BasePlugin):
    def initialize(self):
        self.base_url = self.get_setting('API_BASE_URL')

    def get(self, endpoint, **kwargs):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.get(url, params=kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            raise

    def post(self, endpoint, **kwargs):
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.post(url, json=kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            raise

    def get_setting(self, key, default=None):
        return os.getenv(key, default)