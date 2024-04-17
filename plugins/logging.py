from data_singleton.base import BasePlugin
import logging
import os

class LoggingPlugin(BasePlugin):
    def initialize(self):
        self.log_level = self.get_setting('LOG_LEVEL', 'INFO')
        self.log_file = self.get_setting('LOG_FILE', 'data_singleton.log')
        self.log_format = self.get_setting('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setup_logging()

    def setup_logging(self):
        log_format = self.log_format if self.log_format else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=self.log_level, format=log_format,
                            filename=self.log_file, filemode='a')

    def log_info(self, message):
        logging.info(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_error(self, message):
        logging.error(message)

    def get_setting(self, key, default=None):
        return os.getenv(key, default)