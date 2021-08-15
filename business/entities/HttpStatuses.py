from enum import Enum


class HttpStatuses(Enum):
    """
    Enum class containing some useful http statuses
    @see: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    """

    # 2XX Http Statuses
    """
        Request succeeded.
    """
    OK = 200

    """
        Request succeeded resulting in a new resource being created.
    """
    CREATED = 201

    """
        Request succeeded but no response body is returned.
    """
    NO_CONTENT = 204

    # 4XX Http Statuses
    """
        Request could not be understood by the server due to malformed syntax. The request should
        not be repeated without modifications.
    """
    BAD_REQUEST = 400

    """
        Request requires user authentication.
    """
    UNAUTHORIZED = 401

    """
        The server understood the request, but is refusing to fulfill it.
    """
    FORBIDDEN = 403

    """
        Request URI was not found on the server.
    """
    NOT_FOUND = 404

    # 5XX Http Statuses
    """
        Server encounter an unexpected error while processing the request.
    """
    INTERNAL_SERVER_ERROR = 500
