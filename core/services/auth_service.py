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
    
    
    # ----- Login -----
    def login_user(self, username: str, password:str):
        """
        Attempts to login a user.
        Returns True on success, False on failure.
        """
        user = self.user_model.validate_login(username, password)
        if user:
            self.current_user = user
            return True
        return False
    
    # ----- Logout -----
    def logout_user(self):
        """Logs out the current user."""
        if self.current_user:
            print(f"User '{self.current_user['username']}' logged out.")
        self.current_user = None
        
    # ----- Status -----
    def get_logged_in_user(self):
        """Returns the current logged-in user (SQlite3.Row or None)."""
        return self.current_user
    
    def is_logged_in(self) -> bool:
        """Returns True if a user is logged in."""
        return self.current_user is not None
    
    def is_admin(self) -> bool:
        """Returns True if the current user is an admin."""
        return self.current_user and self.current_user["role"] == "admin"
    
    
'''
- It wraps around the User model, so no duplicate logic can form.
- Maintains session state in memory with self.current_user.
- Returns clean results (True/False) so CLI/UI can decide what to show.
- Compatible with database and current schema 
'''