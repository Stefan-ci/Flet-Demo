import sqlite3, logging
from typing import Optional
from passlib.hash import bcrypt

from utils.settings import DATABASE_PATH
from utils.databases import ProductDBUtil, UserDBUtil


logging.getLogger(__name__)




class DatabaseInterface:
    def __init__(self):
        self.DB_NAME = DATABASE_PATH
        self.CONNECTION = sqlite3.connect(self.DB_NAME, check_same_thread=False)
        self.CURSOR = self.CONNECTION.cursor()
        
        self._products_objects = None
        self._users_objects = None
    
    def close(self):
        if self.CONNECTION:
            self.CURSOR.close()
            self.CONNECTION.close()
    
    def __del__(self):
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



















class DatabaseQuery:
    """ Utility to communicate with the DB """
    
    DB_NAME = DATABASE_PATH
    CONNECTION = sqlite3.connect(DB_NAME, check_same_thread=False)
    CURSOR = CONNECTION.cursor()
    
    
    def __init__(self):
        pass
        
        # Creating tables
        self._create_tables()
    
    def _create_tables(self):
        self.create_user_table()
        self.create_products_table()
    
    def create_user_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                first_name TEXT NULL,
                last_name TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """)
        self.connection.commit()
    
    
    def create_products_table(self):
        fields_sql = ",\n    ".join([f"{name} {definition}" for name, definition in ProductDBUtil().product_fields.items()])
        sql = f"""
            CREATE TABLE IF NOT EXISTS products (
                {fields_sql}
            );
        """
        self.cursor.execute(sql)
        self.connection.commit()
    
    
    
    def _check_user_exists(self, username: str):
        self.cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user:
            return True
        return False
    
    def login_user(self, username: str, password: Optional[str]):
        self.cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        
        if not user:
            return False
        
        if bcrypt.verify(password, user[0]):
            return True
        return False
    
    
    def register_user(self, last_name: str, username: str, password: str, first_name: Optional[str]):
        hashed_password = bcrypt.hash(password) # store the hash, not the raw password
        
        try:
            self.cursor.execute(
                "INSERT INTO users (last_name, username, password, first_name) VALUES (?, ?, ?, ?)",
                (last_name, username, hashed_password, first_name)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error(f"Integrity error: {e}")
            return False
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            return False
    
    
    def create_user(self, last_name: str, username: str, password: str, first_name: Optional[str]):
        return self.register_user(last_name=last_name, username=username, password=password, first_name=first_name)
