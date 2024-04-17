import os
from data_singleton.base import BasePlugin
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class ModelQueryPlugin(BasePlugin):
    def initialize(self):
        self.db_url = self.get_setting('DB_URL')
        if self.db_url is not None:
            self.engine = create_engine(str(self.db_url))
            self.Session = sessionmaker(bind=self.engine)
        else:
            self.engine = None
            self.Session = None

    def query(self, model, **kwargs):
        if self.Session is not None:
            session = self.Session()
            try:
                query = session.query(model)
                for key, value in kwargs.items():
                    query = query.filter(getattr(model, key) == value)
                result = query.first()
                return result
            except Exception:
                raise
            finally:
                session.close()
        else:
            return None

    def get_setting(self, key, default=None):
        return os.getenv(key, default)