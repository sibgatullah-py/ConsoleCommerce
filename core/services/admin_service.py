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

from  core.models.product import Product
from  core.models.order import Order
from  core.models.user import User
# all the dependencies are imported-----------------------------------------------------------------------------------------


class AdminService:
    def __init__(self, db, auth_service: Optional[Any] = None):
        """
        db          : DatabaseManager instance for operation over database
        auth_service: Optional AuthService instance (used for permission checks).
                      If not provided, method wil not enforce admin-only checks.
        """
        self.db = db
        self.auth_service = auth_service
        self.product_model = Product(db)
        self.order_model = Order(db)
        self.user_model = User(db)
        
    
    # ----- Permission Helper -----
    def _ensure_admin(self) -> bool:
        """
        If auth_service was provided, ensures the current user is an admin.
        Returns True if permission is OK (or no auth_service was supplied).
        Returns False if permission denied.
        """
        if not self.auth_service:
            # No auth system provided -- assume caller handles permission
            return True
        
        if not self.auth_service.is_logged_in():
            return False
        
        return self.auth_service.is_admin()
    
    
    # ----- Product management -----
    def add_product(self, name: str, price: float, stock: int = 0, description: str = "") -> bool:
        """
        Add a new product. Admin only (iff auth_service provided).
        Returns True on success, False on failure / permission denied. 
        """
        if not self._ensure_admin():
            return False
        
        return self.product_model.add_product(name, price, stock, description)
    
    def update_product(self, product_id: int, name = None, price = None, stock=None,description=None) -> bool:
        """
        Update an existing product's fields. Fields left as None are not changed.
        """
        if not self._ensure_admin():
            return False
        
        return self.product_model.update_product(product_id, name, price, stock, description)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product by id. Returns True  on success, false on failure / permission denied"""
        if not self._ensure_admin():
            return False
        
        return self.product_model.delete_product(product_id)
    
    def list_product(self) -> list[Dict]:
        """
        Return list of all products. If permission denied, returns empty list. 
        Uses product_model.list_products() which returns sqlite rows (or None).
        """
        if not self._ensure_admin():
            return []
        
        rows = self.product_model.list_products()
        return list(rows) if rows else []
    
    def get_product(self, product_id: int):
        """Return single product row or None."""
        if not self._ensure_admin():
            return None
        return self.product_model.get_by_id(product_id)
    
    
    # ----- Stock helpers -----
    def increase_stock(self, product_id: int, qty: int) -> bool:
        """Increase a product's stock (admin-only if auth is used)."""
        if not self._ensure_admin():
            return False
        return self.product_model.increase_stock(product_id, qty)
    
    def reduce_stock(self, product_id: int, qty: int) -> bool:
        """Increase a product's stock (admin-only if auth is used)."""
        if not self._ensure_admin():
            return False
        return self.product_model.reduce_stock(product_id, qty)
    
    
    # ----- Order confirmation / removal 
    def list_orders(self) -> list[Dict]:
        """Return all orders (admin view)."""
        if not self._ensure_admin():
            return []
        return self.order_model.get_all_orders()
    
    def get_order(self, order_id: int):
        """Return a single order dict or None."""
        if not self._ensure_admin():
            return None 
        return self.order_model.get_order_by_id(order_id)