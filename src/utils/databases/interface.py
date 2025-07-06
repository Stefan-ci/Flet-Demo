import sqlite3
from utils.settings import DATABASE_PATH
from utils.databases import ProductDBUtil, UserDBUtil


class DatabaseInterface:
    def __init__(self):
        self.DB_NAME = DATABASE_PATH
        self.CONNECTION = sqlite3.connect(self.DB_NAME, check_same_thread=False)
        self.CURSOR = self.CONNECTION.cursor()
        
        self._products_objects = None
        self._users_objects = None
    
    def __enter__(self):
        return self
    
    def close(self):
        if self.CONNECTION:
            self.CURSOR.close()
            self.CONNECTION.close()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    
    @property
    def products_objects(self):
        if not self._products_objects:
            self._products_objects = ProductDBUtil(connection=self.CONNECTION, cursor=self.CURSOR)
        return self._products_objects
    
    @property
    def users_objects(self):
        if not self._users_objects:
            self._users_objects = UserDBUtil(connection=self.CONNECTION, cursor=self.CURSOR)
        return self._users_objects
