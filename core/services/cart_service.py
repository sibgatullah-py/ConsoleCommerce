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