import os
import json
import importlib
import logging
import shelve
from dotenv import load_dotenv
from flask import request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class DataSingleton:
    __instance = None

    def __new__(cls):
        if DataSingleton.__instance is None:
            DataSingleton.__instance = super(DataSingleton, cls).__new__(cls)
            DataSingleton.__instance._initialize()
        return DataSingleton.__instance

    def _initialize(self):
        load_dotenv()
        self._config_cache = {}
        self._module_cache = {}
        self._storage_file = os.getenv('STORAGE_FILE', 'data_storage.db')
        self._setup_logging()

    def _setup_logging(self):
        self._log_level = os.getenv('LOG_LEVEL', 'INFO')
        self._log_file = os.getenv('LOG_FILE', 'data_singleton.log')
        self._log_format = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.basicConfig(level=self._log_level, format=self._log_format, filename=self._log_file, filemode='a')

    def _load_config(self, config_file):
        config_path = os.path.join(os.getcwd(), config_file)
        try:
            with open(config_path) as file:
                self._config_cache[config_file] = json.load(file)
        except FileNotFoundError:
            pass

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        def _traverse_attributes(obj, attributes):
            if not attributes:
                return obj
            attr = attributes.pop(0)
            if hasattr(obj, attr):
                return _traverse_attributes(getattr(obj, attr), attributes)
            raise AttributeError(f"'{obj.__class__.__name__}' object has no attribute '{attr}'")

        attributes = name.split('.')
        if attributes[0] == 'config':
            config_file = os.getenv('CONFIG_FILE', 'config.json')
            if config_file not in self._config_cache:
                self._load_config(config_file)
            return _traverse_attributes(self._config_cache[config_file], attributes[1:])
        elif attributes[0] == 'env':
            return os.getenv(attributes[1])
        elif attributes[0] == 'request':
            request_attrs = {
                'form': request.form,
                'headers': request.headers,
                'get_json': request.get_json,
                'args': request.args
            }
            return _traverse_attributes(request_attrs, attributes[1:])
        elif attributes[0] == 'models':
            db_url = os.getenv('DB_URL')
            engine = create_engine(db_url or '')
            Session = sessionmaker(bind=engine)
            session = Session()
            try:
                model_module = importlib.import_module(f"models.{attributes[1]}")
                model = getattr(model_module, attributes[1].capitalize())
                query = session.query(model)
                for attr in attributes[2:]:
                    if attr.isdigit():
                        query = query.filter(getattr(model, 'id') == int(attr))
                    else:
                        query = query.filter(getattr(model, attr))
                return query.first()
            except (ImportError, AttributeError):
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
            finally:
                session.close()
        elif attributes[0] in ['services', 'utils']:
            module_name = '.'.join(attributes[:-1])
            if module_name not in self._module_cache:
                self._module_cache[module_name] = importlib.import_module(module_name)
            return _traverse_attributes(self._module_cache[module_name], attributes[-1:])
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            attributes = name.split('.')
            if len(attributes) == 2 and attributes[0] == 'storage':
                with shelve.open(self._storage_file) as storage:
                    storage[attributes[1]] = value
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def set(self, key, value):
        with shelve.open(self._storage_file) as storage:
            storage[key] = value

    def get(self, key, default=None):
        with shelve.open(self._storage_file) as storage:
            return storage.get(key, default)

    def log_info(self, message):
        logging.info(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_error(self, message):
        logging.error(message)

    def set_bit(self, value, bit_index):
        return value | (1 << bit_index)

    def clear_bit(self, value, bit_index):
        return value & ~(1 << bit_index)

    def is_bit_set(self, value, bit_index):
        return (value >> bit_index) & 1