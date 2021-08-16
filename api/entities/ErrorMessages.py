from enum import Enum


class ErrorMessages(Enum):
    """
    Enum class to keep the known error messages in a single place
    """

    """ Generic Internal Server Error Message """
    INTERNAL_SERVER_ERROR_MESSAGE = "An error occurred while trying to perform the operation."

    """ Resource Not Found Error Message """
    RESOURCE_NOT_FOUND_ERROR_MESSAGE = "The request resource was not found."

    """ Empty Body Error Message """
    EMPTY_BODY_ERROR_MESSAGE = "Data was expected in the body of the request, but none was found"

    """ Error message in case an unknown value is included in the request body """
    UNKNOWN_VALUE_IN_REQUEST_BODY_ERROR_MESSAGE = "An unknown value was found in the request body: {FIELDS}"

    """ Error message in case a request is missing required fields """
    REQUEST_MISSING_REQUIRED_FIELDS_ERROR_MESSAGE = "The following fields were missing from the request body: {FIELDS}"
