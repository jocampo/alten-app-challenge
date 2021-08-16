from enum import Enum


class ReservationFields(Enum):
    """ Collection of fields related to the reservation resource for validation purposes """

    ID = "id"

    GUEST_ID = "guest_id"

    ROOM_ID = "room_id"

    START_DATE = "start_date"

    END_DATE = "end_date"

    AMOUNT_OF_GUESTS = "amount_of_guests"

    STATUS = "status"

    CREATED_AT = "created_at"

    UPDATED_AT = "updated_at"


""" Collection of allowed fields for the POST operation """
ALLOWED_POST_FIELDS = frozenset((
    ReservationFields.GUEST_ID.value,
    ReservationFields.ROOM_ID.value,
    ReservationFields.START_DATE.value,
    ReservationFields.END_DATE.value,
    ReservationFields.AMOUNT_OF_GUESTS.value,
    ReservationFields.STATUS.value,
))

""" Make sure this collection makes sense """
assert all([ReservationFields(x) for x in ALLOWED_POST_FIELDS])

""" Collection of required fields for the POST operation """
REQUIRED_POST_FIELDS = frozenset((
    ReservationFields.GUEST_ID.value,
    ReservationFields.ROOM_ID.value,
    ReservationFields.START_DATE.value,
    ReservationFields.END_DATE.value
))

""" Make sure this collection makes sense """
assert all([ReservationFields(x) for x in REQUIRED_POST_FIELDS])
assert REQUIRED_POST_FIELDS.issubset(ALLOWED_POST_FIELDS)

""" Collection of allowed fields for the PUT operation """
ALLOWED_PUT_FIELDS = frozenset((
    ReservationFields.ID.value,
    ReservationFields.START_DATE.value,
    ReservationFields.END_DATE.value,
    ReservationFields.AMOUNT_OF_GUESTS.value,
    ReservationFields.STATUS.value,
))

""" Make sure this collection makes sense """
assert all([ReservationFields(x) for x in ALLOWED_PUT_FIELDS])

""" Collection of required fields for the PUT operation """
REQUIRED_PUT_FIELDS = frozenset(())

""" Make sure this collection makes sense """
assert all([ReservationFields(x) for x in REQUIRED_PUT_FIELDS])
assert REQUIRED_PUT_FIELDS.issubset(ALLOWED_PUT_FIELDS)
