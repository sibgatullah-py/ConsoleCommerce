'''
This module will handle
    1. Adding/removing items to a user's cart
    2. Viewing cart contents
    3. Checking out (creating an order record in the database)
    
It will work directly with the Product and Order models and use DatabaseManager for query
'''
"""
Handles suer cart operations and order creation.
Each user's cart is stored in memory wile the app runs.
When they checkout, the items are stored in the 'orders' table.
"""

import json
from datetime import datetime
from core.models.product import Product
from core.models.order import Order

class CartService:
    def __init__(self,db):
        self.db = db
        self.carts = {} # in_memory carts: {user_id:{product_id: qty,....}}
        
    # ----- Add to Cart -----
    def add_to_cart(self, user_id: int, product_id:int, qty:int = 1):
        """Add a product to the user's cart."""
        product = Product(self.db).get_by_id(product_id)
        if not product:
            print("Product not found!")
            return False
        
        if product["stock"] <= 0:
            print("Product is out of stock.")
            return False
        
        # Initialize user cart if not exists
        if user_id not in self.carts:
            self.carts[user_id] = {}
            
        # Add quantity
        self.carts[user_id][product_id] = self.carts[user_id].get(product_id, 0)
        print(f"Added {qty} X {product['name']} to your cart.")
        return True
    
    