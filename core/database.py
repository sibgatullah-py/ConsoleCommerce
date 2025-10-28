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
        
        
        
    
        
        