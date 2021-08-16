from enum import Enum


class Routes(Enum):
    """
    Enum class that keeps the routes for the API entities
    """

    """ API routes pertaining operations with the Guest entity """
    GUESTS = "/guests/"

    """ API routes pertaining operations with the Guest entity that require a query parameter"""
    GUESTS_QUERY_PARAMS = f"{GUESTS}<string:guest_id>"

    """ API routes pertaining operations with the Room entity """
    ROOMS = "/rooms/"

    """ API routes pertaining operations with the Room entity that require a query parameter"""
    ROOMS_QUERY_PARAMS = f"{ROOMS}<string:room_id>"

    """ API routes pertaining operations with the Reservation entity """
    RESERVATIONS = "/reservations/"

    """ API routes pertaining operations with the Reservation entity that require a query parameter"""
    RESERVATIONS_QUERY_PARAMS = f"{RESERVATIONS}<string:reservation_id>"

