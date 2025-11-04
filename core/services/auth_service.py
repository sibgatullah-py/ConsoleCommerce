'''
auth_service.py will work as a bridge between the main program like CLI/UI and the model. 
it won't print messages. instead it will return status or objects. 

------------------------------------------------------------------------------------------------------------

Handles user authentication and session management.
Uses the User model for database operations.
'''
from core.models.user import User

class AuthService:
    """Service layer for user authentication and registration."""
    
    def __init__(self,db):
        self.db = db
        self.user_model = User(db)
        self.current_user = None # keeps track of logged-in user row 
        
    # ----- Registration -----
    def register_user(self, username: str, password: str, role:str="customer"):
        """
        Registers a new user.
        Returns True if successful, False if username already exists.
        """
        return self.user_model.register(username, password, role)