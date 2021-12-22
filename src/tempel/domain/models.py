"""
Domain entities.
"""
from datetime import datetime
from typing import Optional
import random
import attr
import time

@attr.s
class User:
    """
    """
    user_id: int = attr.ib(init=False)
    username: str = attr.ib()
    email: str = attr.ib()
    password: str = attr.ib()
    created_at: datetime = attr.ib(default=datetime.now())
    verified: bool = attr.ib(default=False)
    is_active: bool = attr.ib(default=True)
    verify_code: str = attr.ib(init=False)
    expires_on: int = attr.ib(init=False)

    @verify_code.default
    def generate_verify_code(self, digits=6, expires_in=3600) -> str:
        """Retrieves a string with a random integer number format and zeros leading."""
        self.expires_on = int(time.time()) + expires_in
        return f"{random.randint(1, (10**digits)-1):0{digits}d}"

    def verify_user(self, verify_code: str) -> bool:
        """Verifies the given code against the generated code and set verified attribute as true if them match."""
        if not self.verified:
            if self.expires_on < int(time.time()):
                return False
            if self.verify_code != verify_code:
                return False
            self.verified = True
            return True
        return False


@attr.s
class Product:
    """
    """
    # product_id: int = attr.ib(init=False)
    name: str = attr.ib()
    price: float = attr.ib()
    image: str = attr.ib()
    