from flask import jsonify, make_response, request
from flask_restful import Resource, abort
from sqlalchemy.exc import NoResultFound

from api.controllers.custom.CustomFields import ALLOWED_POST_FIELDS, CustomFields, REQUIRED_POST_FIELDS
from api.entities.ErrorMessages import ErrorMessages
from api.entities.HttpStatuses import HttpStatuses
from api.service.ReservationService import ReservationService
from api.service.RoomService import RoomService
from utils.DateUtils import DateUtils


class RoomAvailabilityController(Resource):
    """
    Custom controller to check for room availability
    """
    def post(self):
        """
        Method to handle http POST requests for this route.
        This method checks for the availability of a given Room between the specified start and end dates
        :return: C{True} if the room is available, C{False} otherwise
        """
        self.__validate_post(request.json)
        start_date = DateUtils.convert_str_to_datetime(request.json[CustomFields.START_DATE.value])
        end_date = DateUtils.convert_str_to_datetime(request.json[CustomFields.END_DATE.value])

        # Check that start_date and end_date have tz info. Otherwise, reject the request
        if start_date.tzinfo is None or end_date.tzinfo is None:
            abort(HttpStatuses.BAD_REQUEST.value, message=ErrorMessages.TIMEZONE_MISSING_FROM_DATE_FIELDS.value)

        room_id = request.json[CustomFields.ROOM_ID.value]
        try:
            RoomService.delete(room_id)
        except NoResultFound:
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)

        is_room_available = ReservationService.check_room_availability(room_id, start_date, end_date)
        return make_response(jsonify(is_room_available), HttpStatuses.OK.value)

    def __validate_post(self, post_request: dict):
        """
        Performs validations on the POST request and fails the request if its data has issues
        :param post_request: POST request data
        """
        error_message = ""

        if not isinstance(post_request, dict):
            abort(HttpStatuses.BAD_REQUEST.value)

        if len(post_request.keys()) <= 0:
            error_message = ErrorMessages.EMPTY_BODY_ERROR_MESSAGE.value

        unknown_fields = post_request.keys() - ALLOWED_POST_FIELDS
        if len(unknown_fields) > 0:
            error_message = ErrorMessages.UNKNOWN_VALUE_IN_REQUEST_BODY_ERROR_MESSAGE.value.replace(
                "FIELDS",
                ", ".join(unknown_fields))

        missing_required_fields = REQUIRED_POST_FIELDS - post_request.keys()
        if len(missing_required_fields) > 0:
            error_message = ErrorMessages.REQUEST_MISSING_REQUIRED_FIELDS_ERROR_MESSAGE.value.replace(
                "FIELDS",
                ", ".join(missing_required_fields))

        if error_message:
            abort(HttpStatuses.BAD_REQUEST.value, message=error_message)
