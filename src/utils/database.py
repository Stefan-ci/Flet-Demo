import sqlite3, logging
from typing import Optional
from passlib.hash import bcrypt
# import bcrypt

from utils.settings import DATABASE_PATH

logging.getLogger(__name__)


class DatabaseQuery:
    """ Utility to communicate with the DB """
    def __init__(self):
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        self.create_user_table()
    
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
