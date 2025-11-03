'''
This module is responsible for managing all the products in the database -adding, updating, reading, deleting and managing stock

It does not directly talk to SQLite or MySQL itself, but instead, it uses a helper called db, which is passed to it from outside
That db object handles things like:-
    1. Running SQL queries (SELECT, INSERT etc)
    2. Saving(committing) changes in the database
    3. Returning results (like list or single rows)
So Product focuses on what to do, while db handles how to do it. 
'''

from datetime import datetime

class Product:
    """Handles all product-related database operations."""

    def __init__(self, db):# This saves the DatabaseManager in every instances so every method regarding that isntance/object can talk to database . 
        self.db = db

    # ----- CREATE -----
    def add_product(self, name: str, price: float, stock: int = 0, description: str = "") -> bool:# input type and return type 
        """Add a new product to the database."""
        # The db.execute() runs the query and saves changes by commit = True (remember we kept the commit = False in database.py ?)
        self.db.execute("""
            INSERT INTO products (name, price, stock, description)
            VALUES (?, ?, ?, ?)
        """, (name, float(price), int(stock), description), commit=True)
        # INSERT INTO adds new row to the products table . The ? is a place holder which prevents SQL injection attacks 

        print(f"Product '{name}' added successfully!")
        return True # success signal

    # ----- READ -----
    # These methods returns a Tuple or Dictionary with the products information 
    def get_by_id(self, product_id: int): # Fetches one specific product using its ID
        """Fetch a single product by ID."""
        return self.db.fetch_one("SELECT * FROM products WHERE id = ?", (product_id,)) # id indicates the specific row

    def list_products(self): # Fetch every products from the table 
        """Return all products."""
        return self.db.fetch_all("SELECT * FROM products ORDER BY id ASC") # ORDERED BY id ASC ensures results come in order (ID 1,2,3...)

    def search_products(self, keyword: str):
        """Find products matching a search keyword (name or description)."""
        pattern = f"%{keyword}%" # the % means any number or characters it's like sufix prefix of the key word like (%mouse%) (optical mouse price)
        return self.db.fetch_all(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ?", # LIKE is a SQL keyword for pattern matching 
            (pattern, pattern)
        )

    # ----- UPDATE -----
    # This is a dynamic updater which means it can change one field(column) or multiple or every single one . 
    def update_product(self, product_id: int, name=None, price=None, stock=None, description=None):
        """Update a product's fields dynamically."""
        updates = [] # Holds the SQL parts like 'name = ?, price = ?'
        values = [] # Holds the actual data values like (mouse, 840)

        if name: # if name is given, include it in the update query
            updates.append("name = ?")
            values.append(name)
        if price is not None: # same 
            updates.append("price = ?")
            values.append(float(price))
        if stock is not None: # same 
            updates.append("stock = ?")
            values.append(int(stock))
        if description is not None: # same 
            updates.append("description = ?")
            values.append(description)

        if not updates:
            print("Nothing to update.")
            return False

        values.append(product_id) # after gathering the updated information it adds the product_id to the end of the values list (for the WHERE id = ? part)
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = ?" # building the final SQL query
        self.db.execute(query, tuple(values), commit=True) # executing the query and saving the changes in database 
        print(f"Product ID {product_id} updated successfully.")
        return True

    # ----- DELETE -----
    def delete_product(self, product_id: int):
        """Delete a product from the database."""
        product = self.get_by_id(product_id) # Check if the product exists get_by_id()
        if not product:
            print("Product not found.")
            return False

        self.db.execute("DELETE FROM products WHERE id = ?", (product_id,), commit=True) # this removes the row permanently and commits the changes 
        print(f"Product ID {product_id} deleted successfully.")
        return True

    # ----- STOCK HELPERS -----
    def reduce_stock(self, product_id: int, qty: int):
        """Reduce product stock when an order is placed."""
        product = self.get_by_id(product_id)
        if not product:
            print("Product not found.")
            return False

        current_stock = product["stock"]
        if current_stock < qty:
            print("Not enough products in stock.")
            return False

        self.db.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ?", # subtract the number ordered 
            (qty, product_id), commit=True
        )
        return True

    def increase_stock(self, product_id: int, qty: int):
        """Increase product stock (used when canceling orders)."""
        self.db.execute(
            "UPDATE products SET stock = stock + ? WHERE id = ?", # adds the number of the ordered product back to stock 
            (qty, product_id), commit=True
        )
        return True
