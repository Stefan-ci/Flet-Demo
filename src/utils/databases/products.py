import sqlite3
from typing import Dict
from utils.databases.base import BaseDBUtil
from utils.databases.models import ProductModel


class ProductDBUtil(BaseDBUtil):
    TABLE_NAME = "products"
    MODEL_CLASS = ProductModel
    
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        if not self.TABLE_NAME:
            raise ValueError("TABLE_NAME must be defined.")
        
        super().__init__(connection=connection, cursor=cursor)
    
    
    @property
    def _fields(self) -> Dict[str, str]:
        return {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "code": "TEXT UNIQUE NOT NULL",
            "price": "REAL NOT NULL",
            "details": "TEXT NULL",
            "created_by": "TEXT NULL",
            "created_on": "TEXT DEFAULT CURRENT_TIMESTAMP",
            "is_active": "INTEGER DEFAULT 1",
            "stock": "INTEGER DEFAULT 0",
            "image_url": "TEXT NULL"
        }
