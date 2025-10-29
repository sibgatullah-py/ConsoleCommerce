# core/utils.py (excerpt)

import hashlib

def hash_password(password: str) -> str:
    """Return SHA256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Check if password matches hashed value."""
    return hash_password(password) == hashed
