'''
auth_service.py will work as a bridge between the main program like CLI/UI and the model. 
it won't print messages. instead it will return status or objects. 

------------------------------------------------------------------------------------------------------------

Handles user authentication and session management.
Uses the User model for database operations.
'''

from core.models.user import User