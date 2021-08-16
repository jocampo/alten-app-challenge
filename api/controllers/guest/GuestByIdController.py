from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from api.entities.ErrorMessages import ErrorMessages
from api.entities.HttpStatuses import HttpStatuses
from api.service.GuestService import GuestService

parser = reqparse.RequestParser()
parser.add_argument("guest")


class GuestByIdController(Resource):
    """
    Controller for the Guest resource that require a guest id
    """
    def get(self, guest_id):
        """
        Method to handle http GET requests for this resource, which fetches a single guest
        :param guest_id: id of the guest to be fetched
        :return: HTTP Code indicating the result of the action and the fetched resource
        """
        try:
            guest = GuestService.get_by_id(guest_id)
        except NoResultFound as err:
            # TODO: log error
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)
        # TODO: Return actual object and status code in json (marshmallow?)
        return HttpStatuses.OK.value

    def put(self, guest_id):
        """
        Method to handle http PUT requests for this resource
        :param guest_id: id of the guest to be updated
        :return: Updated entity and HTTP Code indicating the result of the action
        """
        try:
            guest = GuestService.update(guest_id, dict())
        except NoResultFound as err:
            # TODO: log error
            abort(HttpStatuses.NOT_FOUND.value, message=ErrorMessages.RESOURCE_NOT_FOUND_ERROR_MESSAGE.value)
        # TODO: Catch other potential exception types here
        # TODO: Return actual object and status code in json (marshmallow?)
        return HttpStatuses.OK.value

    def delete(self, guest_id):
        """
        Method to handle http DELETE requests for this resource
        :param guest_id: id of the guest to be deleted
        :return: HTTP Code indicating the result of the action
        """
        try:
            GuestService.delete(guest_id)
        except SQLAlchemyError as err:
            # TODO: log error
            abort(HttpStatuses.INTERNAL_SERVER_ERROR.value, message=ErrorMessages.GENERAL_SERVER_ERROR.value)
        return HttpStatuses.OK.value
