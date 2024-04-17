from data_singleton.base import BasePlugin
import os

class EnvPlugin(BasePlugin):
    def get_env(self, key, default=None):
        return os.getenv(key, default)