# core/models/user.py

from datetime import datetime
from core.utils import verify_password # since we aren't hashing the password so we only need this method 

class User:
    """Handles user data and database interactions."""
    
    def __init__(self,db):
        self.db = db
        
        