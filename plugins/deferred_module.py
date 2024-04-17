from data_singleton.base import BasePlugin
import importlib

class DeferredModulePlugin(BasePlugin):
    def initialize(self):
        self.module_cache = {}

    def load_module(self, module_name):
        if module_name not in self.module_cache:
            try:
                module = importlib.import_module(module_name)
                self.module_cache[module_name] = module
            except ImportError:
                raise
        return self.module_cache[module_name]