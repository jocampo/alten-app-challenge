from flask import jsonify, request
from flask_restful import Resource, abort
from sqlalchemy.exc import NoResultFound

from api.controllers.reservation.ReservationFields import ALLOWED_PUT_FIELDS, REQUIRED_PUT_FIELDS, ReservationFields
from api.entities.ErrorMessages import ErrorMessages
from api.entities.HttpStatuses import HttpStatuses
from api.entities.ReservationStatus import ReservationStatus
from api.service.GuestService import GuestService
from api.service.ReservationService import ReservationService
from api.service.RoomService import RoomService


class ReservationByIdController(Resource):
    """
    Controller for the Reservation resource that requires a reservation id
    """
    def get(self, reservation_id: int):
        """
        Method to handle http GET requests for this resource, which fetches a single reservation
        :param reservation_id: id of the reservation to be fetched
        :return: HTTP Code indicating the result of the action and the fetched resource
        """
        reservation = None
        try:
            reservation = ReservationService.get_by_id(reservation_id)
        except NoResultFound:
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)

        return jsonify(reservation)

    def put(self, reservation_id: int):
        """
        Method to handle http PUT requests for this resource
        :param reservation_id: id of the reservation to be updated
        :return: Updated entity and HTTP Code indicating the result of the action
        """
        self.__validate_put(request.json)

        # Convert status field if found in the payload (from string to enum type)
        if ReservationFields.STATUS.value in request.json:
            request.json[ReservationFields.STATUS.value] = ReservationStatus(request.json[ReservationFields.STATUS.value])

        reservation = None
        try:
            ReservationService.update(reservation_id, request.json)
            reservation = ReservationService.get_by_id(reservation_id)
        except NoResultFound:
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)

        return jsonify(reservation)

    def delete(self, reservation_id: int):
        """
        Method to handle http DELETE requests for this resource
        :param reservation_id: id of the reservation to be deleted
        :return: HTTP Code indicating the result of the action. If it succeeds, no body is returned
        """
        try:
            ReservationService.delete(reservation_id)
        except NoResultFound:
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)

        return "", HttpStatuses.NO_CONTENT.value

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

        # Validate linked entities beforehand so we can be explicit about what's missing in the error message
        # should any of them not exist
        if ReservationFields.GUEST_ID.value in update_request:
            guest_id = update_request[ReservationFields.GUEST_ID.value]
            try:
                GuestService.get_by_id(guest_id)
            except NoResultFound:
                error_message = f"Resource Guest with id {guest_id} does not exist. Please provide a valid 'guest_id'"

        if ReservationFields.ROOM_ID.value in update_request:
            room_id = update_request[ReservationFields.ROOM_ID.value]
            try:
                RoomService.get_by_id(room_id)
            except NoResultFound:
                error_message = f"Resource Room with id {room_id} does not exist. Please provide a valid 'room_id'"

        if error_message:
            abort(HttpStatuses.BAD_REQUEST.value, message=error_message)
