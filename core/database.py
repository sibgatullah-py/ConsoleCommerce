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
        self._create_tables()
        self._create_default_admin() # The leading _ means this method is meant to use internally only 
        
        
        
    #------------ Table Creation ------------
    def _create_tables(self):
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
    
    
    #------------ Default Admin Creation ------------>
    
    # def _create_default_admin(self): 
    #     """Creates a default admin user if none exists."""
    #     self.cursor.execute("SELECT * FROM users WHERE role='admin'")
    #     admin_exists = self.cursor.fetchone()
    #     if not admin_exists: # if no row were found , it creates one . 
    #         self.cursor.execute(
    #             "INSERT INTO users (username, password, role) VALUES (?,?,?)",('admin','admin123','admin'),
               
    #         )
    #         self.conn.commit() # saving the changes in database . 
       
            
    def _create_default_admin(self):# defines a private method . which runs automatically when the Database class is initialized.
        """Bootstrap one default admin if none exists."""
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")# looking for any row with the role admin . if none is found returns nothing
        admin_count = self.cursor.fetchone()[0]# fetchone() retrives the first row from the query result in line 71. returns None if no row were found

        if admin_count == 0:
            print("[INIT] Creating default admin account...")

            username = "admin"
            password = "admin123"
            created_at = datetime.now().isoformat(timespec="seconds")
            # ?,?,? is parameterized query syntax in SQLite, it prevents SQL injection and makes the code more secure and clean
            self.cursor.execute("""
                INSERT INTO users (username, password, role, created_at)
                VALUES (?, ?, 'admin', ?)
            """, (username, password, created_at))
            self.conn.commit()

            print(" Default admin created! (username: admin, password: admin123)")