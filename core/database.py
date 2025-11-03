'''
Database works:->
    1. Open the database by making a connection
    2. Create room(table) inside
    3. Add, find, update or delete things in the table
    4. Commit the changes and close the database connection
'''

import sqlite3 # The python sqlite3 library file
import os # helps to work with folder and file path
from datetime import datetime # helps to record current date time for 

class DatabaseManager: # this class acts as a manager which will manage our database after it's created .
    """
    High-level wrapper for SQLite database operations.
    Handles initialization, table creation, query execution,
    and safe admin bootstrapping.
    """

    def __init__(self, db_path: str = "data/ecommerce.db"): # This constructor will run autometically when a new db is created . if no db is assigned it will create a db in "data/ecomerce.db" by default as database
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True) # checking if the data folder exists if not then creates the data folder

        self.db_path = db_path # it remembers the database file location so it can use the path later
        self.conn = sqlite3.connect(self.db_path) # connecting with the database file like opening the database 
        self.conn.row_factory = sqlite3.Row  # access results by column name. This tells SQLite to give query results as dictionary-like objects.
        self.cursor = self.conn.cursor() # a cursor is like a pen that writes database commands and executes commands 

        # Initialize tables and default admin . the _ before the method name as prefix means this method is only used in backend
        self._create_tables() # creates all table
        self._create_default_admin() # creates a default superuser admin

    # ------------ Table Creation ------------
    def _create_tables(self): # This is a secret helper function (that’s what the _ means)
        """Create all required tables if they do not already exist."""

        # Users
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'customer',
                created_at TEXT
            )
        """)

        # Products
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                description TEXT
            )
        """)

        # Orders
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                items_json TEXT,
                status TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """) # items_json means a list of items in JSON format
        # The Foreign key part tells SQLite that user_id must match a real id from the users table-- it links two tables together 

        self.conn.commit() # Saving the changes permanently

    # ------------ Default Admin Creation ------------
    def _create_default_admin(self): # Secret helper function for creating a super user
        """Bootstrap a default admin account if none exists."""
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")# This looks inside the users table and counts how many admins exists.
        admin_count = self.cursor.fetchone()[0] # fetches one row and gets the index number i guess

        if admin_count == 0:
            print("Creating default admin account...")
            # built in admin 
            username = "admin"
            password = "admin123"  # Stored as plain text
            created_at = datetime.now().isoformat(timespec="seconds") # this says when the built in admin was activated 

            # This adds the default admin information in the database ---
            self.cursor.execute("""
                INSERT INTO users (username, password, role, created_at)
                VALUES (?, ?, 'admin', ?)
            """, (username, password, created_at))
            self.conn.commit()
            # ----------------------------------------------------------
            print("Default admin created! (username: admin, password: admin123)")

    # ------------ General Query Execution ------------
    '''
    in line 104-> This is a universal command runner. Instade of writing lots of SQL by hand, i can call db.execute("SELECT * FROM users").
    it takes:-
        1. query   : My SQL text
        2. params  : Any values i want to insert safely
        3. And flags like (fetchone), (fetchall), (commit) to control what the database does next
    '''
    def execute(self, query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
        """Execute an SQL query safely with parameters."""
        try: # This tries to run my SQL commands safely
            self.cursor.execute(query, params)
            if commit: # if i say commit in any file or place it saves the commit in the database 
                self.conn.commit()
            if fetchone: # if i ask one row anywhere in project it gives one desired row
                return self.cursor.fetchone()
            if fetchall: # if i ask all the rows of a table anywhere in the project it gives all the available rows 
                return self.cursor.fetchall()
            
        except sqlite3.Error as e: # If anything goes wrong then  it cathces the error and instade of crashing the program it gives and error message
            print(f"[DB ERROR] {e}")
            return None

    # Optional helper wrappers
    def fetch_one(self, query, params=()): # a shortcut method for fetching one row
        return self.execute(query, params, fetchone=True)

    def fetch_all(self, query, params=()):# a shortcut method for fetching all the row
        return self.execute(query, params, fetchall=True)

    # ------------ Context Manager Support ------------
    '''
    These makes it possible to use the (with) statement like ( with DatabaseManager() as db: )
    '''
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ------------ Connection Close ------------
    def close(self): # Method for closing the connection
        """Close database connection safely."""
        if self.conn:
            self.conn.close()
