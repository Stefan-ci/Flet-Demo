import sqlite3
from typing import Type, Dict
from pydantic import BaseModel


class BaseDBUtil:
    TABLE_NAME = None
    MODEL_CLASS: Type[BaseModel] = None
    
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.connection = connection
        self.cursor = cursor
        
        # create table auto in subclass
        self.create_table()
    
    @property
    def _fields(self) -> Dict[str, str]:
        raise NotImplementedError("Define fields in the subclass.")
    
    
    def create_table(self):
        fields_sql = ",\n    ".join([f"{name} {definition}" for name, definition in self._fields.items()])
        sql = f"""CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
            {fields_sql}
        );"""
        self.cursor.execute(sql)
        self.connection.commit()
        
        # Missing cols
        self.add_missing_columns()
    
    
    def get_existing_columns(self) -> Dict[str, str]:
        self.cursor.execute(f"PRAGMA table_info({self.TABLE_NAME});")
        return {col[1]: col[2] for col in self.cursor.fetchall()}
    
    
    def add_missing_columns(self):
        existing_columns = self.get_existing_columns()
        for name, definition in self._fields.items():
            if name not in existing_columns:
                self.cursor.execute(f"ALTER TABLE {self.TABLE_NAME} ADD COLUMN {name} {definition};")
        self.connection.commit()
    
    
    def get_column_names(self):
        self.cursor.execute(f"PRAGMA table_info({self.TABLE_NAME});")
        return [col[1] for col in self.cursor.fetchall()]
    
    
    def _to_pydantic_model(self, row):
        if self.MODEL_CLASS:
            return self.MODEL_CLASS(**dict(zip(self.get_column_names(), row)))
        raise NotImplementedError("MODEL_CLASS must be defined for this table.")
    
    
    def create(self, **kwargs):
        keys = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?"] * len(kwargs))
        values = list(kwargs.values())
        sql = f"INSERT INTO {self.TABLE_NAME} ({keys}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.connection.commit()
        row_id = self.cursor.lastrowid
        return self.get(id=row_id)
    
    
    def update(self, id: int, **kwargs):
        if not kwargs:
            raise ValueError("No fields to update provided.")
        set_clause = ", ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values())
        values.append(id)
        sql = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE id=?"
        self.cursor.execute(sql, values)
        self.connection.commit()
        return self.get(id=id)
    
    
    def delete(self, id: int):
        sql = f"DELETE FROM {self.TABLE_NAME} WHERE id=?"
        self.cursor.execute(sql, (id,))
        self.connection.commit()
    
    
    def exists(self, **kwargs):
        """Check if at least one record exists with the given conditions."""
        if not kwargs:
            raise ValueError("Conditions required for 'exists'")
        conditions = " AND ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values())
        sql = f"SELECT 1 FROM {self.TABLE_NAME} WHERE {conditions} LIMIT 1"
        self.cursor.execute(sql, values)
        return self.cursor.fetchone() is not None
    
    
    def count(self, **kwargs) -> int:
        """Count number of rows optionally matching a condition."""
        if kwargs:
            conditions = " AND ".join([f"{k}=?" for k in kwargs])
            values = list(kwargs.values())
            sql = f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE {conditions}"
            self.cursor.execute(sql, values)
        else:
            sql = f"SELECT COUNT(*) FROM {self.TABLE_NAME}"
            self.cursor.execute(sql)
        return self.cursor.fetchone()[0]
    
    
    def all(self):
        self.cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
        rows = self.cursor.fetchall()
        # return [dict(zip(self.get_column_names(), row)) for row in rows]
        return [self._to_pydantic_model(row) for row in rows]
    
    
    
    def filter(self, **kwargs):
        """ Return a list of rows matching the given filters. """
        if not kwargs:
            return self.all()
        
        conditions = " AND ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values())
        
        self.cursor.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE {conditions}", values)
        rows = self.cursor.fetchall()
        return [self._to_pydantic_model(row) for row in rows]
    
    
    def get(self, **kwargs):
        """ Return a single row matching the given condition (or None). """
        if not kwargs:
            raise ValueError("You must specify at least one condition")
        conditions = " AND ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values())
        
        self.cursor.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE {conditions} LIMIT 1", values)
        row = self.cursor.fetchone()
        if row:
            return self._to_pydantic_model(row)
        return None
