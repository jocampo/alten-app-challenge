from enum import Enum


class ReservationStatus(Enum):
    """
    Enum class holding all the possible Reservation statuses
    """

    """
    The reservation is scheduled, this is the default status for a new reservation
    """
    SCHEDULED = 'SCHEDULED'

    """
    The reservation has been canceled, it can be uncanceled as long as it doesn't conflict with a SCHEDULED one
    """
    CANCELED = 'CANCELED'
