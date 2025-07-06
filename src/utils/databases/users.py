import sqlite3
from typing import Dict, Optional
from utils.databases.base import BaseDBUtil
from utils.databases.models import UserModel
from utils.security.generics import hash_str, check_hash, needs_rehash


class UserDBUtil(BaseDBUtil):
    TABLE_NAME = "users"
    MODEL_CLASS = UserModel
    
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        if not self.TABLE_NAME:
            raise ValueError("TABLE_NAME must be defined.")
        
        super().__init__(connection=connection, cursor=cursor)
    
    
    @property
    def _fields(self) -> Dict[str, str]:
        return {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "username": "TEXT UNIQUE NOT NULL",
            "email": "TEXT NULL", # can be unique or not
            "first_name": "TEXT NULL",
            "last_name": "TEXT NOT NULL",
            "password": "TEXT NOT NULL",
            "is_active": "INTEGER DEFAULT 1 CHECK (is_active IN (0, 1))",
            "is_admin": "INTEGER DEFAULT 0 CHECK (is_admin IN (0, 1))",
            "created_on": "TEXT DEFAULT CURRENT_TIMESTAMP"
        }
    
    
    def create_user(self, **kwargs):
        return self.create(**kwargs)
    
    
    def create(self, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = hash_str(secret=kwargs["password"])
        return super().create(**kwargs)
    
    
    def login(self, username: str, password: Optional[str]):
        if not self.exists(username=username):
            return False
        
        user: UserModel = self.get(username=username)
        if not user:
            return False
        
        if not user._is_active:
            return False
        
        return self.check_user_password(user=user, input_password=password)
    
    
    def set_as_admin(self, username: str):
        user: UserModel = self.get(username=username)
        if user:
            self.update(id=user.id, is_admin=True, is_active=True)
        return user
    
    
    def check_user_password(self, user: UserModel, input_password: str):
        if not check_hash(user.password, input_password):
            return False
        
        if needs_rehash(user.password):
            new_hash = hash_str(input_password)
            self.update(id=user.id, password=new_hash)
        
        return True
