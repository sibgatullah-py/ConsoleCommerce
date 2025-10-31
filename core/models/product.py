# core/models/product.py

from datetime import datetime

class Product:
    '''Handles all product-related database operations.'''
    
    def __init__(self,db):# db is the DatabaseManager instance, giving access to .execute() just like the cursor 
        self.db = db
        
    # Now the CRUD system starts from here --->
    
    # ----- CREATE ----->
    def add_product(self,name:str,price:float,stock: int = 0,description: str = "") -> bool:
        '''Add a new product in the database table (products)'''
        created_at = datetime.now().isoformat(timespec="seconds")
        
        self.db.execute("""
                        INSERT INTO products (name, price, stock, description)
                        VALUES (?,?,?,?)
                        """,
                        (name, float(price), int(stock), description),
                        commit = True
                        )
        
        print(f"Product {name} added successfully!")
        return True