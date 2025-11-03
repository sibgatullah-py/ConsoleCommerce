from datetime import datetime

class User:
    """Handles user data and database interactions."""

    def __init__(self, db):
        self.db = db  # DatabaseManager instance

    # ----- Register User -----
    def register(self, username: str, password: str, role: str = "customer") -> bool:
        """Register a new user if username is not already taken."""
        existing = self.get_by_username(username)
        if existing:
            print("Username already exists!")
            return False

        created_at = datetime.now().isoformat(timespec="seconds")

        # Store password as plain text
        self.db.execute("""
            INSERT INTO users (username, password, role, created_at)
            VALUES (?, ?, ?, ?)
        """, (username, password, role, created_at), commit=True)

        print(f"User '{username}' registered successfully!")
        return True

    # ----- Login Validation -----
    def validate_login(self, username: str, password: str):
        """Check if username and password are valid."""
        user = self.get_by_username(username)
        if not user:
            print("User not found.")
            return None

        if password == user["password"]:
            print(f"Welcome back, {user['username']}!")
            return user
        else:
            print("Incorrect password.")
            return None

    # ----- Fetch User -----
    def get_by_username(self, username: str):
        """Fetch a user by username."""
        return self.db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))

    def get_by_id(self, user_id: int):
        """Fetch a user by ID."""
        return self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
