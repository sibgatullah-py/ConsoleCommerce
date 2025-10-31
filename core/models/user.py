# core/models/user.py

from datetime import datetime # let us use current date time.
from core.utils import verify_password # since we aren't hashing the password so we only need this method 

class User: # Building an user object. this method is for user tasks (register, login, fetch)
    """Handles user data and database interactions."""
    # This constructor means the User object now knows how to talk to the database-- through self.db
    def __init__(self,db):# why ? If we want to load a user's info, save updates or delete a user, all these actions needs to interact with the database. 
        self.db = db # here self.db is the phone line to the database . without it the user class wouldn't know where to save or fetch anything. This is how the method talks with the database 
        
    #----- Register user ----->
    def register(self, username: str, password:str, role: str = "customer") -> bool:
        """register a new user if username is not already taken."""
        existing = self.get_by_username(username)
        if existing :
            print("Username already exists !")
            return False
        
        created_at = datetime.now().isoformat(timespec='seconds')
        
        # store password directly plain text no hashing 
        self.db.execute("""
                        INSERT INTO users (username, password, role, created_at)
                        VALUES (?,?,?,?)
                        """) # this is the same as cursor.execute() just when we call cursor after defining it we are doing this same thing as db.execute()
        
        print(f"User '{username}' registered successfully!")
        return True
        
        
    #----- Login Validation ----->
    def validate_login(self, username:str, password:str):
        """Check if username and password are valid."""
        
        user = self.get_by_username(username)
        if not user:
            print('User not found')
            return None
        
        if verify_password(password, user['password']):
            print("Welcome Back, {user['username']}!")
            return user
        else:
            print("Incorrect Password.")
            return None
        
    #----- Fetch User ----->
    def get_by_username(self, username: str):
        """Fetch a user by username"""
        result = self.db.fetch_one("SELECT * FROM users WHERE username = ?",(username,))
        return result
    