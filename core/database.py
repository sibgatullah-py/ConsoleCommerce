import sqlite3
import os
import json
from datetime import datetime
import hashlib


class DatabaseManager:
    '''
    High-level wrapper for SQLite database operations.
    Handles initialization, table creation, query execution, and safe admin bootstrapping.
    '''
    # database file creation method ->
    def __init__(self, db_path: str = 'data/ecommerce.db'):
        # ensure /data directory exists
        os.makedirs(os.path.dirname(db_path),exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)# Connects to the DQLite database file at the given path on line 14 . if not exist then sql creates one 
        self.cursor = self.conn.cursor() # creates a cursor object for executing SQL queries on that database 
        
        # initialize tables and admin account 
        self.create_tables()
        self.create_default_admin()
        
        
        
    #------------ Table Creation ------------
    def create_tables(self):
        '''Create all required tables if they do not already exists.'''
        
        # user table
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL,
                                role TEXT DEFAULT 'customer',
                                created_at TEXT
                            )
                            """)
        
        # products table
        self.cursor.execute("""
                            CRATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                stock INTEGER DEFAULT 0,
                                description TEXT
                            )
                            """)
        
        # Order Table
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                items_json TEXT,
                                created_at TEXT,
                                FOREIGN KEY (user_id) REFERENCES users(id)
                            )
                            """)
        
        self.conn.commit()
    