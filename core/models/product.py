from datetime import datetime

class Product:
    """Handles all product-related database operations."""

    def __init__(self, db):
        self.db = db

    # ----- CREATE -----
    def add_product(self, name: str, price: float, stock: int = 0, description: str = "") -> bool:
        """Add a new product to the database."""
        self.db.execute("""
            INSERT INTO products (name, price, stock, description)
            VALUES (?, ?, ?, ?)
        """, (name, float(price), int(stock), description), commit=True)

        print(f"Product '{name}' added successfully!")
        return True

    # ----- READ -----
    def get_by_id(self, product_id: int):
        """Fetch a single product by ID."""
        return self.db.fetch_one("SELECT * FROM products WHERE id = ?", (product_id,))

    def list_products(self):
        """Return all products."""
        return self.db.fetch_all("SELECT * FROM products ORDER BY id ASC")

    def search_products(self, keyword: str):
        """Find products matching a search keyword (name or description)."""
        pattern = f"%{keyword}%"
        return self.db.fetch_all(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ?",
            (pattern, pattern)
        )

    # ----- UPDATE -----
    def update_product(self, product_id: int, name=None, price=None, stock=None, description=None):
        """Update a product's fields dynamically."""
        updates, values = [], []

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
            print("Nothing to update.")
            return False

        values.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = ?"
        self.db.execute(query, tuple(values), commit=True)
        print(f"Product ID {product_id} updated successfully.")
        return True

    # ----- DELETE -----
    def delete_product(self, product_id: int):
        """Delete a product from the database."""
        product = self.get_by_id(product_id)
        if not product:
            print("Product not found.")
            return False

        self.db.execute("DELETE FROM products WHERE id = ?", (product_id,), commit=True)
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
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            (qty, product_id), commit=True
        )
        return True

    def increase_stock(self, product_id: int, qty: int):
        """Increase product stock (used when canceling orders)."""
        self.db.execute(
            "UPDATE products SET stock = stock + ? WHERE id = ?",
            (qty, product_id), commit=True
        )
        return True
