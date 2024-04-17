from data_singleton.base import BasePlugin
import shelve
import os

class StoragePlugin(BasePlugin):
    def initialize(self):
        storage_file = self.get_setting('STORAGE_FILE', 'data_storage.db')
        if not isinstance(storage_file, str):
            raise ValueError("STORAGE_FILE setting must be a string")
        self.storage_file = storage_file

    def set(self, key, value):
        with shelve.open(self.storage_file) as storage:
            storage[key] = value

    def get(self, key, default=None):
        with shelve.open(self.storage_file) as storage:
            return storage.get(key, default)

    def get_setting(self, key, default=None):
        return os.getenv(key, default)