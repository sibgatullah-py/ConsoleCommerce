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
    
    def update_order_status(self, order_id: int, new_status: str)-> bool:
        """
        Updata an order status. Handles 'cancled' specially: if an order is cancelled,
        this method attempts to restore product stock for each item in the order (only if it wasn't cancelled before).
        Returns True on success, False on failure or permission denied. 
        """
        if not self._ensure_admin(): # making sure the user is an admin
            return False
        
        order = self.order_model.get_order_by_id(order_id)
        if not order:
            return False
        
        old_status = order['status']
        
        # if cancelling, restore stock for items of old_status wasn't already cancelled 
        if new_status.lower() == "cancelled" and old_status.lower() != 'cancelled':
            # restore stock per item
            for item in order['items']:
                pid  = item.get("product_id")
                qty = item.get("qty",0)
                if pid and qty:
                    # Best-effort: ignorefailures restoring stock but continue 
                    self.product_model.increase_stock(pid,qty)
                    
        # Update the order status in DB
        try:
            # The Order.update_order method expects new_items list or new_status
            self.order_model.update_order(order_id, new_items=None, new_status=new_status)
            return True
        except Exception:
            return False
        
    
    # Canceling and Deleting order methods
    def cancel_order(self, order_id: int) -> bool:
        """
        Convenience method to cancel an order (sets status to 'cancelled' and restores stock).
        """
        return self.update_order_status(order_id, 'cancelled')
    
    def delete_order(self, order_id:int) -> bool:
        """
        Permanently6 delete an order record 
        """
        if not self._ensure_admin():
            return False
        
        order = self.order_model.get_order_by_id(order_id)
        if not order:
            return False
        
        # Optionally : restore stock if deleting a pending/processing order
        # For safety, we will not automatically restore stock here (admin can call increase_stock manually)
        try:
            self.order_model.delete_order(order_id)
            return True
        except Exception:
            return False
            
            
    # ----- User Administration -----
    def promote_user_to_admin(self,user_id:int)-> bool:
        """
        Change user's role to 'admin' from customer, returns True on success.
        """
        if not self._ensure_admin():
            return False
        
        user = self.user_model.get_by_id(user_id)
        if not user:
            return False
        
        # Reuse Product.update_product style: dynamic update
        try:
            self.db.execute("UPDATE users SET role = 'admin' WHERE id = ?",(user_id))
            return True
        except Exception:
            return False
        
    def demote_admin_to_customer(self,user_id:int) -> bool:
        """
        Demote an admin back to customer. Prevent demoting the last admin if desired
        """
        if not self._ensure_admin():
            return False
        
        user = self.user_model.get_by_id(user_id)
        if not user:
            return False
        
        # Prevent demoting yourself via auth_service
        if self.auth_service and self.auth_service.is_logged_in():
            current = self.auth_service.get_logged_in_user()
            # Don't allow demoting the current logged-in admin
            if current and current['id'] == user_id:
                return False
            
        try:
            self.db.execute("UPDATE users SET role = 'customer' WHERE id = ?",(user_id))
            return True
        except Exception:
            return False
        
        
    # ----- Admin report helpers ----- 
    def product_count(self) -> int:
        """
        Returns number of products (admin only if auth provided )
        """
        if not self._ensure_admin():
            return 0
        rows = self.db.fetchone("SELECT COUNT(* as c FROM products")
        return rows['c'] if rows else 0
    
    def order_count(self) -> int:
        """
        returns total number of orders
        """
        if not self._ensure_admin():
            return 0
        rows = self.db.fetchone("SELECT COUNT(*) as c FROM orders")
        return rows['c'] if rows else 0
    
    