from enum import Enum


class GuestFields(Enum):
    """ Collection of fields related to the guest resource for validation purposes """

    ID = "id"

    DOCUMENT = "document"

    FIRST_NAME = "first_name"

    LAST_NAME = "last_name"

    IS_ACTIVE = "is_active"

    CREATED_AT = "created_at"

    UPDATED_AT = "updated_at"

""" Collection of allowed fields for the POST operation """
ALLOWED_POST_FIELDS = frozenset((
    GuestFields.DOCUMENT.value,
    GuestFields.FIRST_NAME.value,
    GuestFields.LAST_NAME.value
))

""" Collection of required fields for the POST operation """
REQUIRED_POST_FIELDS = frozenset((
    GuestFields.DOCUMENT.value,
    GuestFields.FIRST_NAME.value,
    GuestFields.LAST_NAME.value
))

""" Collection of allowed fields for the PUT operation """
ALLOWED_PUT_FIELDS = frozenset((
    GuestFields.DOCUMENT.value,
    GuestFields.FIRST_NAME.value,
    GuestFields.LAST_NAME.value,
    GuestFields.IS_ACTIVE.value
))

""" Collection of required fields for the PUT operation """
REQUIRED_PUT_FIELDS = frozenset(())
