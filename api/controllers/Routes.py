from enum import Enum


class Routes(Enum):
    """
    Enum class that keeps the routes for the API entities
    """
    """ Pre-fix for all API URLs """
    API_BASE = "/api/v1"

    """ API routes pertaining operations with the Guest entity """
    GUESTS = f"{API_BASE}/guests"

    """ API routes pertaining operations with the Guest entity by id """
    GUESTS_BY_ID = f"{GUESTS}<string:guest_id>"

    """ API routes pertaining operations with the Room entity """
    ROOMS = f"{API_BASE}/rooms"

    """ API routes pertaining operations with the Room entity by id """
    ROOMS_BY_ID = f"{ROOMS}<string:room_id>"

    """ API routes pertaining operations with the Reservation entity """
    RESERVATIONS = f"{API_BASE}/reservations"

    """ API routes pertaining operations with the Reservation entity by id """
    RESERVATIONS_BY_ID = f"{RESERVATIONS}<string:reservation_id>"

