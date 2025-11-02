import json
from datetime import datetime

class Order:
    """Handles all order-related operations."""

    def __init__(self, db):
        self.db = db

    # ----- CREATE -----
    def create_order(self, user_id: int, items: list):
        """Create a new order for a specific user."""
        items_json = json.dumps(items)
        created_at = datetime.now().isoformat(timespec="seconds")
        status = "pending"

        self.db.execute("""
            INSERT INTO orders (user_id, items_json, status, created_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, items_json, status, created_at), commit=True)

        print("Order created successfully.")

    # ----- READ -----
    def get_user_orders(self, user_id: int):
        """Fetch all orders placed by a specific user."""
        rows = self.db.fetch_all("SELECT * FROM orders WHERE user_id = ?", (user_id,))
        return [self._row_to_dict(row) for row in rows] if rows else []

    def get_all_orders(self):
        """Fetch all orders (admin view)."""
        rows = self.db.fetch_all("SELECT * FROM orders")
        return [self._row_to_dict(row) for row in rows] if rows else []

    def get_order_by_id(self, order_id: int):
        """Fetch a single order by ID."""
        row = self.db.fetch_one("SELECT * FROM orders WHERE id = ?", (order_id,))
        if not row:
            print(f"No order found with ID {order_id}.")
            return None
        return self._row_to_dict(row)

    # ----- UPDATE -----
    def update_order(self, order_id: int, new_items: list = None, new_status: str = None):
        """Update an order's items or status."""
        existing = self.get_order_by_id(order_id)
        if not existing:
            return

        updated_items = json.dumps(new_items) if new_items else json.dumps(existing["items"])
        updated_status = new_status if new_status else existing["status"]

        self.db.execute("""
            UPDATE orders SET items_json = ?, status = ? WHERE id = ?
        """, (updated_items, updated_status, order_id), commit=True)

        print(f"Order {order_id} updated successfully.")

    # ----- DELETE -----
    def delete_order(self, order_id: int):
        """Delete an order from the system by its ID."""
        order = self.get_order_by_id(order_id)
        if not order:
            return

        self.db.execute("DELETE FROM orders WHERE id = ?", (order_id,), commit=True)
        print(f"Order {order_id} deleted successfully.")

    # ----- Helper -----
    def _row_to_dict(self, row):
        """Convert an SQLite row to a dictionary."""
        try:
            items = json.loads(row["items_json"])
        except json.JSONDecodeError:
            items = []

        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "items": items,
            "status": row["status"],
            "created_at": row["created_at"]
        }
