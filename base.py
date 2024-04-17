import importlib
import os
from dotenv import load_dotenv

class BasePlugin:
    def __init__(self):
        self.load_settings_from_env()

    def initialize(self):
        pass

    def load_settings_from_env(self):
        load_dotenv()

class DataSingleton:
    __instance = None

    def __new__(cls):
        if DataSingleton.__instance is None:
            DataSingleton.__instance = super(DataSingleton, cls).__new__(cls)
            DataSingleton.__instance._initialize_plugins()
        return DataSingleton.__instance

    def _initialize_plugins(self):
        plugins_folder = os.path.join(os.path.dirname(__file__), 'plugins')
        for file_name in os.listdir(plugins_folder):
            if file_name.endswith('.py') and file_name != '__init__.py':
                module_name = file_name[:-3]
                module = importlib.import_module(f'data_singleton.plugins.{module_name}')
                plugin_class = getattr(module, f'{module_name.capitalize()}Plugin')
                plugin_instance = plugin_class()
                plugin_instance.initialize()
                setattr(self, f'_{module_name}', plugin_instance)

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        def _traverse_attributes(obj, attributes):
            if len(attributes) == 0:
                return obj
            attr = attributes.pop(0)
            if hasattr(obj, attr):
                return _traverse_attributes(getattr(obj, attr), attributes)
            else:
                raise AttributeError(f"'{obj.__class__.__name__}' object has no attribute '{attr}'")

        attributes = name.split('.')
        plugin_name = attributes[0]
        plugin_attribute = '_' + plugin_name

        if hasattr(self, plugin_attribute):
            plugin_instance = getattr(self, plugin_attribute)
            return _traverse_attributes(plugin_instance, attributes[1:])
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{plugin_name}'")