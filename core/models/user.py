'''
This file talks with the the database through the DatabaseManager class to:-
    1. Create new users
    2. Check if someone can log in 
    3. Fetch user details by username or ID
    
This is a bridge between the modules and the database tables
'''

from datetime import datetime

class User: # class for Register new user, Check their login, Find the user in database
    """Handles user data and database interactions."""

    def __init__(self, db): # giving every user a databsemanager to communicate with the database
        self.db = db  # DatabaseManager instance

    # ----- Register User -----
    def register(self, username: str, password: str, role: str = "customer") -> bool: # This method takes str input and returns bool type value
        """Register a new user if username is not already taken."""
        existing = self.get_by_username(username)
        if existing: # Check if the user with same information exists 
            print("Username already exists!")
            return False

        created_at = datetime.now().isoformat(timespec="seconds") # get the date and time of the user creation 

        # Insert new user into the database and Store password as plain text
        self.db.execute("""
            INSERT INTO users (username, password, role, created_at)
            VALUES (?, ?, ?, ?)
        """, (username, password, role, created_at), commit=True)

        print(f"User '{username}' registered successfully!")
        return True

    # ----- Login Validation -----
    def validate_login(self, username: str, password: str):
        """Check if username and password are valid."""
        user = self.get_by_username(username) # checking if the username exists in the database 
        if not user:
            print("User not found.")
            return None

        if password == user["password"]: # Compare the password if it matches the pass in databse user table
            print(f"Welcome back, {user['username']}!")
            return user
        else:
            print("Incorrect password.")
            return None

    # ----- Fetch User -----
    # These are smaller helper methods that makes other parts of this app easier and dynamic 
    
    def get_by_username(self, username: str):
        """Fetch a user by username."""
        return self.db.fetch_one("SELECT * FROM users WHERE username = ?", (username,)) # fetches one user by user name

    def get_by_id(self, user_id: int):
        """Fetch a user by ID."""
        return self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,)) # fetches one user by user ID
