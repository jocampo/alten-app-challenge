from enum import Enum


class CustomFields(Enum):
    """ Collection of fields related to the custom controllers for validation purposes """

    ROOM_ID = "room_id"

    START_DATE = "start_date"

    END_DATE = "end_date"


""" Collection of allowed fields for the POST operation """
ALLOWED_POST_FIELDS = frozenset((
    CustomFields.ROOM_ID.value,
    CustomFields.START_DATE.value,
    CustomFields.END_DATE.value,
))

""" Make sure this collection makes sense """
assert all([CustomFields(x) for x in ALLOWED_POST_FIELDS])

""" Collection of required fields for the POST operation """
REQUIRED_POST_FIELDS = frozenset((
    CustomFields.ROOM_ID.value,
    CustomFields.START_DATE.value,
    CustomFields.END_DATE.value,
))

""" Make sure this collection makes sense """
assert all([CustomFields(x) for x in REQUIRED_POST_FIELDS])
assert REQUIRED_POST_FIELDS.issubset(ALLOWED_POST_FIELDS)
