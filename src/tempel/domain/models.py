"""
Domain entities.
"""
from datetime import datetime
from typing import Optional
import random

class User:
    def __init__(self, username: str, email: str, password: str):
        self.user_id: int
        self.username: str = username
        self.email: str = email
        self.password: str = password
        self.created_at: DateTime = datetime.now()
        self.verify_code: str = self.generate_verify_code(6)
        self.verified: bool = False
        self.is_active: bool = True

    def generate_verify_code(self, digits: int) -> str:
        """Retrieves a string with a random integer number format."""
        return f"{random.randint(1, (10**digits)-1):0{digits}d}"

    def verify_user(self, verify_code: str) -> bool:
        """Verifies the given code against the generated code and set verified attribute as true if them match."""
        if self.verify_code == verify_code:
            self.verified = True
            return True
        return False