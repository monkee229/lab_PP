from datetime import datetime
from typing import List

from models import User, Booking, BookingStatus
from exceptions import BookingException, UserNotFoundException, BookingNotFoundException, InvalidDateException
from repositories import Repository


class UserService:
    def __init__(self, repository: Repository) -> None:
        self._repository: Repository = repository

    def create_user(self, user: User) -> User:
        try:
            user.user_id = f"U{len(self.list_users()) + 1}"
            self._repository.create(user)
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            raise BookingException(f"Failed to create user: {str(e)}")

    def get_user(self, user_id: str) -> User:
        user = self._repository.read(user_id)
        if not user or not isinstance(user, User):
            raise UserNotFoundException(f"User {user_id} not found.")
        return user

    def update_user(self, user: User) -> User:
        try:
            self.get_user(user.user_id)
            self._repository.update(user)
            return user
        except Exception as e:
            print(f"Error updating user: {e}")
            raise BookingException(f"Failed to update user: {str(e)}")

    def delete_user(self, user_id: str) -> None:
        try:
            self.get_user(user_id)
            self._repository.delete(user_id)
        except Exception as e:
            print(f"Error deleting user: {e}")
            raise BookingException(f"Failed to delete user: {str(e)}")

    def list_users(self) -> List[User]:
        return [p for p in self._repository.list_all() if isinstance(p, User)]


class BookingService:
    def __init__(self, repository: Repository) -> None:
        self._repository: Repository = repository

    def _calculate_price(self, property_price: float, check_in: datetime, check_out: datetime) -> float:
        nights = (check_out - check_in).days
        if nights <= 0:
            nights = 1
        return round(property_price * nights, 2)

    def create_booking(self, booking: Booking) -> Booking:
        try:
            # Валидация дат
            if booking.check_in_date >= booking.check_out_date:
                raise InvalidDateException("Check-out date must be after check-in date.")
            if booking.check_in_date < datetime.now():
                raise InvalidDateException("Check-in date cannot be in the past.")

            booking.booking_id = f"B{len(self.list_bookings()) + 1}"
            booking.total_price = self._calculate_price(
                booking.property.price_per_night,
                booking.check_in_date,
                booking.check_out_date
            )
            booking.status = BookingStatus.PENDING

            self._repository.create(booking)
            return booking
        except InvalidDateException:
            raise
        except Exception as e:
            print(f"Error creating booking: {e}")
            raise BookingException(f"Failed to create booking: {str(e)}")

    def get_booking(self, booking_id: str) -> Booking:
        booking = self._repository.read(booking_id)
        if not booking or not isinstance(booking, Booking):
            raise BookingNotFoundException(f"Booking {booking_id} not found.")
        return booking

    def update_booking_status(self, booking_id: str, status: BookingStatus) -> None:
        try:
            booking = self.get_booking(booking_id)
            booking.update_status(status)
            self._repository.update(booking)
        except Exception as e:
            print(f"Error updating booking status: {e}")
            raise BookingException(f"Failed to update booking status: {str(e)}")

    def delete_booking(self, booking_id: str) -> None:
        try:
            self.get_booking(booking_id)  # Проверка
            self._repository.delete(booking_id)
        except Exception as e:
            print(f"Error deleting booking: {e}")
            raise BookingException(f"Failed to delete booking: {str(e)}")

    def list_bookings(self) -> List[Booking]:
        return [a for a in self._repository.list_all() if isinstance(a, Booking)]