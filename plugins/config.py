from data_singleton.base import BasePlugin
import json
import os

class ConfigPlugin(BasePlugin):
    def initialize(self):
        self.config_cache = {}
        self.config_file = self.get_setting('CONFIG_FILE', 'config.json')
        self.load_config()

    def load_config(self):
        config_path = os.path.join(os.getcwd(), str(self.config_file))
        try:
            with open(config_path) as file:
                self.config_cache = json.load(file)
        except FileNotFoundError:
            pass

    def get_config(self, key, default=None):
        return self.config_cache.get(key, default)

    def get_setting(self, key, default=None):
        return os.getenv(key, default)