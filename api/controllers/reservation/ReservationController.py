from flask import jsonify, make_response, request
from flask_restful import Resource, abort
from sqlalchemy.exc import NoResultFound

from api.controllers.reservation.ReservationFields import ALLOWED_POST_FIELDS, REQUIRED_POST_FIELDS, ReservationFields
from api.entities.APIErrors import ReservationError
from api.entities.ErrorMessages import ErrorMessages
from api.entities.HttpStatuses import HttpStatuses
from api.entities.ReservationStatus import ReservationStatus
from api.service.GuestService import GuestService
from api.service.ReservationService import ReservationService
from api.service.RoomService import RoomService


class ReservationController(Resource):
    """
    Controller for the Reservation resource
    """
    def get(self):
        """
        Method to handle http GET requests for this resource, which fetches all reservations
        :return: HTTP Code indicating the result of the action and the fetched resources
        """
        return jsonify(ReservationService.get_all())

    def post(self):
        """
        Method to handle http POST requests for this resource
        :return: HTTP Code indicating the result of the action and the newly created entity
        """
        self.__validate_post(request.json)

        # Convert status field if found in the payload (from string to enum type)
        if ReservationFields.STATUS.value in request.json:
            request.json[ReservationFields.STATUS.value] = ReservationStatus(request.json[ReservationFields.STATUS.value])

        reservation = None
        try:
            reservation_id = ReservationService.create(request.json)
            reservation = ReservationService.get_by_id(reservation_id)
        except ReservationError as res_error:
            abort(HttpStatuses.BAD_REQUEST.value, message=res_error.args[0])
        except NoResultFound:
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)

        return make_response(jsonify(reservation), HttpStatuses.CREATED.value)

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

        # Validate linked entities beforehand so we can be explicit about what's missing in the error message
        # should any of them not exist
        if ReservationFields.GUEST_ID.value in create_request:
            guest_id = create_request[ReservationFields.GUEST_ID.value]
            try:
                GuestService.get_by_id(guest_id)
            except NoResultFound:
                error_message = f"Resource Guest with id {guest_id} does not exist. Please provide a valid 'guest_id'"

        if ReservationFields.ROOM_ID.value in create_request:
            room_id = create_request[ReservationFields.ROOM_ID.value]
            try:
                RoomService.get_by_id(room_id)
            except NoResultFound:
                error_message = f"Resource Room with id {room_id} does not exist. Please provide a valid 'room_id'"

        if error_message:
            abort(HttpStatuses.BAD_REQUEST.value, message=error_message)
