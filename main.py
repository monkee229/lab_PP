from datetime import datetime
from typing import List

from models import BookingStatus, Address, User, Property, Booking
from repositories import InMemoryRepository
from services import UserService, BookingService
from serializers import JSONSerializer, XMLSerializer
from exceptions import UserNotFoundException, BookingNotFoundException, InvalidDateException, BookingException


def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Ошибка: Дата должна быть в формате YYYY-MM-DD (e.g., 2025-10-01)")
        return None


def parse_status(status_str: str) -> BookingStatus:
    status_str = status_str.lower()
    if status_str == "pending":
        return BookingStatus.PENDING
    elif status_str == "confirmed":
        return BookingStatus.CONFIRMED
    elif status_str == "cancelled":
        return BookingStatus.CANCELLED
    else:
        print("Ошибка: Статус 'pending', 'confirmed' или 'cancelled'")
        return None


def serialize_data(user_service: UserService, booking_service: BookingService):
    json_serializer = JSONSerializer()
    xml_serializer = XMLSerializer()
    try:
        json_serializer.to_file(user_service.list_users(), "users.json")
        xml_serializer.to_file(booking_service.list_bookings(), "bookings.xml")
        print("Данные сохранены в users.json и bookings.xml")
    except BookingException as e:
        print(f"Ошибка сериализации: {e}")


def cli_mode(user_service: UserService, booking_service: BookingService):

    addr_template = Address("123 Main St", "New York", "10001")
    property_template = Property("P1", "Cozy Apartment", addr_template, 150.00)

    while True:
        command = input("\n> ").strip().split()
        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "exit":
            print("Выход.")
            break

        elif cmd == "help":
            print("Доступные команды: add_user, list_users, get_user <id>, delete_user <id>, "
                  "add_booking, list_bookings, get_booking <id>, update_status <id> <status>, "
                  "delete_booking <id>, serialize, help, exit")

        elif cmd == "add_user":
            first_name = input("  Имя: ").strip()
            last_name = input("  Фамилия: ").strip()
            email = input("  Email: ").strip()

            user = User(first_name, last_name, email, addr_template, "")
            try:
                created = user_service.create_user(user)
                print(f"Пользователь добавлен: {created.get_full_name()} (ID: {created.user_id})")
                serialize_data(user_service, booking_service)
            except Exception as e:
                print(f"Ошибка: {e}")

        elif cmd == "list_users":
            users = user_service.list_users()
            if not users:
                print("Список пользователей пуст.")
            else:
                print(f"Пользователи ({len(users)}):")
                for u in users:
                    print(f"  - {u.get_full_name()} (ID: {u.user_id}), Email: {u.email}")

        elif cmd == "get_user" and len(command) > 1:
            user_id = command[1]
            try:
                got = user_service.get_user(user_id)
                print(f"Пользователь {user_id}: {got.get_full_name()}")
            except UserNotFoundException as e:
                print(f"{e}")

        elif cmd == "delete_user" and len(command) > 1:
            user_id = command[1]
            confirm = input(f"Удалить пользователя {user_id}? (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    user_service.delete_user(user_id)
                    print(f"Пользователь {user_id} удалён.")
                    serialize_data(user_service, booking_service)
                except Exception as e:
                    print(f"Ошибка удаления: {e}")

        elif cmd == "add_booking":
            user_id = input("  ID пользователя: ").strip()
            try:
                user = user_service.get_user(user_id)
            except UserNotFoundException:
                print("Пользователь не найден.")
                continue

            check_in_str = input("  Дата заезда (YYYY-MM-DD): ").strip()
            check_in = parse_date(check_in_str)
            if not check_in:
                continue

            check_out_str = input("  Дата выезда (YYYY-MM-DD): ").strip()
            check_out = parse_date(check_out_str)
            if not check_out:
                continue

            print(f"Бронирование жилья: {property_template.name} (ID: {property_template.property_id})")
            booking = Booking("", user, property_template, check_in, check_out)

            try:
                created = booking_service.create_booking(booking)
                print(f"Бронь добавлена: ID {created.booking_id} с {created.check_in_date.date()} "
                      f"по {created.check_out_date.date()}, Цена: ${created.total_price}")
                serialize_data(user_service, booking_service)
            except (InvalidDateException, BookingException) as e:
                print(f"{e}")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif cmd == "list_bookings":
            bookings = booking_service.list_bookings()
            if not bookings:
                print("Список бронирований пуст.")
            else:
                print(f"Бронирования ({len(bookings)}):")
                for b in bookings:
                    print(f"  - {b.booking_id}: {b.user.get_full_name()} -> {b.property.name} "
                          f"({b.check_in_date.date()} - {b.check_out_date.date()}, {b.status.value})")

        elif cmd == "get_booking" and len(command) > 1:
            booking_id = command[1]
            try:
                got = booking_service.get_booking(booking_id)
                print(
                    f"Бронь {booking_id}: {got.user.get_full_name()} на {got.check_in_date.date()} ({got.status.value})")
            except BookingNotFoundException as e:
                print(f"{e}")

        elif cmd == "update_status" and len(command) > 2:
            booking_id = command[1]
            status_str = command[2]
            status = parse_status(status_str)
            if not status:
                continue
            try:
                booking_service.update_booking_status(booking_id, status)
                print(f"Статус брони {booking_id} обновлён на {status.value}")
                serialize_data(user_service, booking_service)
            except BookingNotFoundException as e:
                print(f"{e}")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif cmd == "delete_booking" and len(command) > 1:
            booking_id = command[1]
            confirm = input(f"Удалить бронь {booking_id}? (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    booking_service.delete_booking(booking_id)
                    print(f"Бронь {booking_id} удалена.")
                    serialize_data(user_service, booking_service)
                except Exception as e:
                    print(f"Ошибка удаления: {e}")

        elif cmd == "serialize":
            serialize_data(user_service, booking_service)

        else:
            print("Неизвестная команда. Введите 'help' для списка.")


if __name__ == "__main__":
    user_repo = InMemoryRepository()
    booking_repo = InMemoryRepository()
    user_service = UserService(user_repo)
    booking_service = BookingService(booking_repo)

    print("=== Запуск приложения ===")

    addr = Address("123 Main St", "New York", "10001")
    demo_users = [
        User("Alice", "Malise", "alice@example.com", addr, ""),
        User("Bob", "Big", "bob@example.com", addr, "")
    ]
    for u in demo_users:
        user_service.create_user(u)
    print(f"Созданы {len(user_service.list_users())} демо-пользователей.")

    cli_mode(user_service, booking_service)

    print("\nПриложение завершено!")