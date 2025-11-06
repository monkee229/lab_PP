from __future__ import annotations
from typing import Dict, Any
from datetime import datetime

from .base import BookingStatus
from .user import User
from .property import Property


class Booking:
    def __init__(
            self,
            booking_id: str,
            user: User,
            property_obj: Property,
            check_in_date: datetime,
            check_out_date: datetime,
            status: BookingStatus = BookingStatus.PENDING
    ) -> None:
        self.booking_id: str = booking_id
        self.user: User = user
        self.property: Property = property_obj
        self.check_in_date: datetime = check_in_date
        self.check_out_date: datetime = check_out_date
        self.status: BookingStatus = status
        self.total_price: float = 0.0

    def update_status(self, new_status: BookingStatus) -> None:
        self.status = new_status

    def to_dict(self) -> Dict[str, Any]:
        return {
            'booking_id': self.booking_id,
            'user_id': self.user.user_id,
            'property_id': self.property.property_id,
            'check_in_date': self.check_in_date.isoformat(),
            'check_out_date': self.check_out_date.isoformat(),
            'status': self.status.value,
            'total_price': self.total_price
        }