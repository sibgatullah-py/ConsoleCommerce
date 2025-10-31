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
    
    # ----- READ ----->
    def get_by_id(self,product_id:int):
        """Fetch one product by it's ID"""
        return self.db.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id),
            fetchone = True
        )
        
    def list_products(self):
        """return all products"""
        return self.db.execute(
            "SELECT * FROM products ORDERED BY id ASC",
            fetchall = True
        )
        
    def search_products(self, keyword: str):
        """Find products matching a search keyword ( name or description )"""
        pattern = f"%{keyword}%"
        return self.db.execute(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ?",
            (pattern, pattern),
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