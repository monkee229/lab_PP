from typing import Dict, Any
from .base import Address


class Property:
    def __init__(
            self,
            property_id: str,
            name: str,
            address: Address,
            price_per_night: float
    ) -> None:
        self.property_id: str = property_id
        self.name: str = name
        self.address: Address = address
        self.price_per_night: float = price_per_night

    def to_dict(self) -> Dict[str, Any]:
        return {
            'property_id': self.property_id,
            'name': self.name,
            'address': self.address.to_dict(),
            'price_per_night': self.price_per_night
        }