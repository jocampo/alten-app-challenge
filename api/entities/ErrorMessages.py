from enum import Enum


class ErrorMessages(Enum):
    """
    Enum class to keep the known error messages in a single place
    """

    """ Generic Internal Server Error Message """
    INTERNAL_SERVER_ERROR_MESSAGE = 'An error occurred while trying to perform the operation.'

    """ Resource Not Found Error Message """
    RESOURCE_NOT_FOUND_ERROR_MESSAGE = 'The request resource was not found.'

