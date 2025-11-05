# core/services/admin_service.py

"""
AdminService
------------

Service layer that provides administrative operations over products, orders, and users.
Designed to work with existing models:
    - core.models.product.Product
    - core.models.order.Order
    - core.models.user.User
    
It accepts a DatabaseManager instance and (optionally) an AuthService instance for permission check.
Methods return booleans or model objects/rows consistent with the rest of the project so the UI/CLI can decide what to display.

Security notes (not implemented here, but will work on later):
    1. Stop storing plaintext passwords and use hashing + salt
    2. Add proper audit logging for admin actions
"""

'''
The typing module allows to indicate the expected types of variables(int str etc), function parameters and return values.
It provides tools and features for adding type hints. 
'''
from typing import Optional, Any, List, Dict  