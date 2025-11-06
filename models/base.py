from enum import Enum
from typing import Dict, Any

class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Address:
    def __init__(self, street: str, city: str, postal_code: str) -> None:
        self.street: str = street
        self.city: str = city
        self.postal_code: str = postal_code

    def to_dict(self) -> Dict[str, str]:
        return {
            'street': self.street,
            'city': self.city,
            'postal_code': self.postal_code
        }

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.postal_code}"