from typing import List, Dict, Any
from .base import Address

class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        address: Address,
        user_id: str = ""
    ) -> None:
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.address: Address = address
        self.user_id: str = user_id
        self.bookings: List['Booking'] = []

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'address': self.address.to_dict(),
        }