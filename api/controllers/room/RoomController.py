from flask import jsonify, make_response, request
from flask_restful import Resource, abort
from sqlalchemy.exc import NoResultFound

from api.controllers.room.RoomFields import ALLOWED_POST_FIELDS, REQUIRED_POST_FIELDS
from api.entities.ErrorMessages import ErrorMessages
from api.entities.HttpStatuses import HttpStatuses
from api.service.RoomService import RoomService


class RoomController(Resource):
    """
    Controller for the Room resource
    """
    def get(self):
        """
        Method to handle http GET requests for this resource, which fetches all rooms
        :return: HTTP Code indicating the result of the action and the fetched resources
        """
        return jsonify(RoomService.get_all())

    def post(self):
        """
        Method to handle http POST requests for this resource
        :return: HTTP Code indicating the result of the action and the newly created entity
        """
        self.__validate_post(request.json)

        room = None
        try:
            room_id = RoomService.create(request.json)
            room = RoomService.get_by_id(room_id)
        except NoResultFound:
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)

        return make_response(jsonify(room), HttpStatuses.CREATED.value)

    def __validate_post(self, create_request: dict):
        """
        Performs validations on the POST request and fails the request if its data has issues
        :param create_request: POST request data
        """
        error_message = ""

        if not isinstance(create_request, dict):
            abort(HttpStatuses.BAD_REQUEST.value)

        if len(create_request.keys()) <= 0:
            error_message = ErrorMessages.EMPTY_BODY_ERROR_MESSAGE.value

        unknown_fields = create_request.keys() - ALLOWED_POST_FIELDS
        if len(unknown_fields) > 0:
            error_message = ErrorMessages.UNKNOWN_VALUE_IN_REQUEST_BODY_ERROR_MESSAGE.value.replace(
                "FIELDS",
                ", ".join(unknown_fields))

        missing_required_fields = REQUIRED_POST_FIELDS - create_request.keys()
        if len(missing_required_fields) > 0:
            error_message = ErrorMessages.REQUEST_MISSING_REQUIRED_FIELDS_ERROR_MESSAGE.value.replace(
                "FIELDS",
                ", ".join(missing_required_fields))

        if error_message:
            abort(HttpStatuses.BAD_REQUEST.value, message=error_message)
