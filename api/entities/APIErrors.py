"""
Collection of errors that we can catch and identify exactly what went wrong
"""


class ReservationError(Exception):
    """ When there are issues related to the Reservation trying to be created/updated """
    pass
