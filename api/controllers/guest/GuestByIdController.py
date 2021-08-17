from flask_restful import Resource, abort
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from flask import request, jsonify

from api.controllers.guest.GuestFields import ALLOWED_PUT_FIELDS, REQUIRED_PUT_FIELDS
from api.entities.ErrorMessages import ErrorMessages
from api.entities.HttpStatuses import HttpStatuses
from api.service.GuestService import GuestService


class GuestByIdController(Resource):
    """
    Controller for the Guest resource that requires a guest id
    """
    def get(self, guest_id: int):
        """
        Method to handle http GET requests for this resource, which fetches a single guest
        :param guest_id: id of the guest to be fetched
        :return: HTTP Code indicating the result of the action and the fetched resource
        """
        try:
            guest = GuestService.get_by_id(guest_id)
        except NoResultFound:
            # TODO: log error
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)
        # TODO: Return actual object and status code in json (marshmallow?)
        return jsonify(guest)

    def put(self, guest_id: int):
        """
        Method to handle http PUT requests for this resource
        :param guest_id: id of the guest to be updated
        :return: Updated entity and HTTP Code indicating the result of the action
        """
        self.__validate_put(request.json)
        try:
            guest = GuestService.update(guest_id, request.json)
        except NoResultFound as err:
            # TODO: log error
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)
        # TODO: Catch other potential exception types here
        # TODO: Return actual object and status code in json (marshmallow?)
        return HttpStatuses.OK.value

    def delete(self, guest_id: int):
        """
        Method to handle http DELETE requests for this resource
        :param guest_id: id of the guest to be deleted
        :return: HTTP Code indicating the result of the action
        """
        try:
            GuestService.delete(guest_id)
        except NoResultFound:
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)
        except SQLAlchemyError:
            # TODO: log error
            abort(HttpStatuses.INTERNAL_SERVER_ERROR.value, message=ErrorMessages.GENERAL_SERVER_ERROR.value)
        return HttpStatuses.OK.value

    def __validate_put(self, update_request: dict):
        """
        Performs validations on the PUT request and fails the request if its data has issues
        :param update_request: PUT request data
        """
        error_message = ""

        if not isinstance(update_request, dict):
            abort(HttpStatuses.BAD_REQUEST.value)

        if len(update_request.keys()) <= 0:
            error_message = ErrorMessages.EMPTY_BODY_ERROR_MESSAGE.value

        unknown_fields = update_request.keys() - ALLOWED_PUT_FIELDS
        if len(unknown_fields) > 0:
            error_message = ErrorMessages.UNKNOWN_VALUE_IN_REQUEST_BODY_ERROR_MESSAGE.value.replace(
                "FIELDS",
                ", ".join(unknown_fields))

        missing_required_fields = REQUIRED_PUT_FIELDS - update_request.keys()
        if len(missing_required_fields) > 0:
            error_message = ErrorMessages.REQUEST_MISSING_REQUIRED_FIELDS_ERROR_MESSAGE.value.replace(
                "FIELDS",
                ", ".join(missing_required_fields))

        if error_message:
            abort(HttpStatuses.BAD_REQUEST.value, message=error_message)

