'''
This class is responsible for handling all actions related to orders in the database-- creating, reading, updating and deleting

It talks to the database through an object called db, which is passed when this class is created and every instance of this class inharites this 
So the class doesn't directly talks with the SQL, it asks the db object to do that . 
'''

import json # used to convert Python data (like lists or dicts) into a string for storing in the database, and back again when reading 
from datetime import datetime

class Order:
    """Handles all order-related operations."""
    # The constructor runs once when the class is created 
    def __init__(self, db):# The db argument is an object that knows how to run DQL commands
        self.db = db # stores the db object inside the class so every method can use it to communicate with the database

    # ----- CREATE -----
    def create_order(self, user_id: int, items: list): # this method creates a new orders in the orders table
        """Create a new order for a specific user."""
        items_json = json.dumps(items)# Converts the items list(object) into a JSON string so it can be stored in a single database column
        created_at = datetime.now().isoformat(timespec="seconds") # .isoformat() makes the date time readable and easy to store in database 
        status = "pending"

        # This adds a new record to the orders table, ? are placeholders for the values commit = True means save the changes in the database 
        self.db.execute("""
            INSERT INTO orders (user_id, items_json, status, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, items_json, status, created_at), commit=True)

        print("Order created successfully.")

    # ----- READ -----
    def get_user_orders(self, user_id: int):
        """
        Fetch all orders placed by a specific user.
        1. runs a query to find all rows where user_id matches
        2. fetch_all() returns a list of rows
        3. each row is converted into a dictionary using _row_to_dict() for easier working 
        """
        rows = self.db.fetch_all("SELECT * FROM orders WHERE user_id = ?", (user_id,)) # the fetch_all() method is located in database.py
        return [self._row_to_dict(row) for row in rows] if rows else [] # if there are no orders, it returns an empty list [] note: list comprehension and ternary operators are used here 

    def get_all_orders(self): 
        """Fetch all orders (admin view). Shows all orders of every users"""
        rows = self.db.fetch_all("SELECT * FROM orders")
        # using regular looping and if else condition instead of list comprehension and ternary operators 
        result = []
        if rows:
            for row in rows:
                result.append(self._row_to_dict(row))
        else:
            result = []
        
        return result
            

    def get_order_by_id(self, order_id: int):
        """Fetch a single order by ID."""
        row = self.db.fetch_one("SELECT * FROM orders WHERE id = ?", (order_id,)) # fetch_one() returns a single row
        if not row:
            print(f"No order found with ID {order_id}.")
            return None
        return self._row_to_dict(row)

    # ----- UPDATE -----
    def update_order(self, order_id: int, new_items: list = None, new_status: str = None):
        """Update an order's items or status."""
        existing = self.get_order_by_id(order_id) # getting the existing orders
        if not existing:
            return
        # if new items were provided it converts them into JSON with json.dumps(new_item) otherwise it keeps the existing one 
        updated_items = json.dumps(new_items) if new_items else json.dumps(existing["items"])
        updated_status = new_status if new_status else existing["status"] # if a new status was given, use that 
        # update the database
        self.db.execute("""
            UPDATE orders SET items_json = ?, status = ? WHERE id = ?
        """, (updated_items, updated_status, order_id), commit=True)

        print(f"Order {order_id} updated successfully.")

    # ----- DELETE -----
    def delete_order(self, order_id: int):
        """Delete an order from the system by its ID."""
        order = self.get_order_by_id(order_id) # checks if the order exists 
        if not order:
            return

        self.db.execute("DELETE FROM orders WHERE id = ?", (order_id,), commit=True) # delete the order by holding the ID which will remove the row 
        print(f"Order {order_id} deleted successfully.")



    # ----- Helper -----
    def _row_to_dict(self, row):
        """Convert an SQLite row to a dictionary."""
        try:# json.loads() converts the json string into a python dictionary/list
            items = json.loads(row["items_json"]) # row["items_json"] is a string like [{"product_id":5,"qty":2}]
        except json.JSONDecodeError:
            items = []

        return { # This makes sure every order is always returned in the same nice format 
            "id": row["id"],
            "user_id": row["user_id"],
            "items": items,
            "status": row["status"],
            "created_at": row["created_at"]
        }


'''
The order gets saved in database like this 

id-1        user_id-2       items_json-[{"product_id":5,"qty": 3}]      status-pending      Created_at-2025-11-03T20:45:00

'''