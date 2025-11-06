class BookingException(Exception):
    pass

class UserNotFoundException(BookingException):
    pass

class PropertyNotFoundException(BookingException):
    pass

class BookingNotFoundException(BookingException):
    pass

class InvalidDateException(BookingException):
    pass

class PropertyUnavailableException(BookingException):
    pass