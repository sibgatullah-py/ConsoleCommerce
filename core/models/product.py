# core/models/product.py

from datetime import datetime # imports the datetime class from python's built-in module called datetime.

class Product: # this class is the blueprint as it will be used to create product objects also read update and delete them 
    '''Handles all product-related database operations.'''
    
    # This is the constructor -- a special method that runs auto whenever we create a new product object.
    def __init__(self,db):# This is our database connection. db is the DatabaseManager instance, giving access to .execute() just like the cursor .
        self.db = db # here we're saving the DatabaseManager/db inside the product object itself.
        # Think it as a line of connection that connects our product object to the SQL database and giving us access on the operation over that product/obj

        
    # Now the CRUD system starts from here -------------------------------->
    
    # ----- CREATE ----->
    def add_product(self,name:str,price:float,stock: int = 0,description: str = "") -> bool: # requests those information for the parameters and returns bool type output
        '''Add a new product in the database table (products)'''
        created_at = datetime.now().isoformat(timespec="seconds")
        
        self.db.execute("""
                        INSERT INTO products (name, price, stock, description)
                        VALUES (?,?,?,?) 
                        """,# the ? placeholder actually prevents SQL injection hacking 
                        (name, float(price), int(stock), description), # This tuple gives the actual values 
                        commit = True # save the changes permanently in the database (mandatory)
                        )
        
        print(f"Product {name} added successfully!") # a success message 
        return True # telling the program the operation work correctly 
    
    # ----- READ ----->
    def get_by_id(self,product_id:int): # Fetch a single product 
        """Fetch one product by it's ID"""
        return self.db.execute(
            "SELECT * FROM products WHERE id = ?", # this tells the db, Find me the product whose id equals the number i gave 
            (product_id,),# This is actually a tuple notice the comma ? it's how Python passes a single value into SQL
            fetchone = True # This means only want one row . the first one to match the id i gave 
        )
        
    def list_products(self): # No parameters cause we want to see all the products
        """return all products"""
        return self.db.execute(
            "SELECT * FROM products ORDERED BY id ASC", # Get all product sorted by their id in ascending order. 
            fetchall = True # This returns a list of rows . each rows are a product . 
        )
        
    def search_products(self, keyword: str): # Find a product by keyword 
        """Find products matching a search keyword ( name or description )"""
        pattern = f"%{keyword}%" # In SQL, the % sign means any text before and after like suffix and prefix %mouse% .
        return self.db.execute(
            # LIKE is SQL's version of fuzzy searching
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ?",# find all the products where the name or des looks like my keyword
            (pattern, pattern), # use %keyword% for both name and description
            fetchall = True
        )
        
        
    # ----- UPDATE ----->
    def update_product(self, product_id: int, name=None, price=None, stock=None, description=None):
        """Update a product's fields dynamically."""
        updates = []
        values = []
        
        if name:
            updates.append("name = ?")
            values.append(name)
        if price is not None:
            updates.append("price = ?")
            values.append(float(price))
        if stock is not None:
            updates.append("stock = ?")
            values.append(int(stock))
        if description is not None:
            updates.append("description = ?")
            values.append(description)
            
        if not updates:
            print("nothing to update")
            return False
        
        
        values.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = ?"
        
        self.db.execute(query, tuple(values), commit = True)
        print(f"Product ID {product_id} updated successfully")
        return True
    
    # ----- DELETE ----->
    def delete_product(self, product_id: int):
        """Delete a product from the database"""
        product = self.get_by_id(product_id)
        if not product:
            print("Product not found.")
            return False
        
        self.db.execute("DELETE FROM products WHERE id = ?",(product_id,),commit = True)
        print(f" Product ID {product_id} deleted successfully")
        return True