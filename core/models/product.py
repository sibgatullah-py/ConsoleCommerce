# core/models/product.py

from datetime import datetime

class Product:
    '''Handles all product-related database operations.'''
    
    def __init__(self,db):# db is the DatabaseManager instance, giving access to .execute() just like the cursor 
        self.db = db