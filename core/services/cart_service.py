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
    
    
    # ----- Remove from Cart -----
    def remove_from_cart(self, user_id:int,product_id:int):
        """Remove a product entirely from the cart using the product ID"""
        if user_id not in self.carts or product_id not in self.carts[user_id]:
            print("Product not in your cart")
            return False
        
        del self.carts[user_id][product_id]
        print("Product has been removed from your cart.")
        return True
    
    
    # ----- View Cart ----- 
    def view_cart(self, user_id: int):
        """Show all items in the user's cart"""
        if user_id not in self.carts or not self.carts[user_id]:
            print("Your cart is empty.")
            return []
        
        print("\n--- Your Cart ---")
        total = 0
        for product_id, qty in self.carts[user_id].items():
            product = Product(self.db).get_by_id(product_id)
            subtotal = product["price"] * qty
            print(f"{product['name']} (x{qty}) - ${subtotal:.2f}")
            total += subtotal
        print(f"Total: ${total: .2f}")
        return self.carts[user_id]
    
    
    # ----- Checkout -----
    def checkout(self, user_id: int):
        """Convert cart to order and clear it."""
        if user_id not in self.carts or not self.carts[user_id]:
            print("Cart is empty. Nothing to checkout.")
            return False
        
        items = []
        for pid, qty in self.carts[user_id].items():
            product = Product(self.db).get_by_id(pid)
            if not product:
                continue
            items.append({
                'product_id':pid,
                'name':product['name'],
                'price':product['price'],
                'qty':qty,
            })
            
        # Create an order record
        order_model = Order(self.db)
        order_model.create_order(user_id,items)
        
        # Clear cart
        del self.carts[user_id]
        print("Checkout completed! Your order has been placed.")
        return True
    
    
'''
How it works:
    - Keeps each user's cart in memory -> {user_id: {product_id: qty}}
    - Uses the Product model to check product details 
    - Uses the Order model to create an order during checkout 
    - Provides clean methods:
        1. add_to_cart()
        2. remove_from_cart()
        3. view_cart()
        4. checkout() 
'''