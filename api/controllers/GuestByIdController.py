from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from api.entities.ErrorMessages import ErrorMessages
from api.entities.HttpStatuses import HttpStatuses
from api.service.GuestService import GuestService
from flask import request


parser = reqparse.RequestParser()
parser.add_argument("guest")


class GuestByIdController(Resource):
    """
    Controller for the Guest resource that require query params
    """
    def get(self):
        """
        Method to handle http GET requests for this resource, which fetches all guests
        :return: HTTP Code indicating the result of the action and the fetched resource
        """
        try:
            guests = GuestService.get_all()
        except SQLAlchemyError as err:
            # TODO: log error
            abort(HttpStatuses.INTERNAL_SERVER_ERROR.value, message=ErrorMessages.INTERNAL_SERVER_ERROR_MESSAGE.value)
        # TODO: Return actual objects and status code in json (marshmallow?)
        return HttpStatuses.OK.value

    def post(self):
        """
        Method to handle http POST requests for this resource
        :return: HTTP Code indicating the result of the action and the newly created entity
        """
        thing = request.form['data']
        try:
            guest = GuestService.create(dict())
        except SQLAlchemyError as err:
            # TODO: log error
            abort(HttpStatuses.INTERNAL_SERVER_ERROR.value, message=ErrorMessages.INTERNAL_SERVER_ERROR_MESSAGE.value)
        # TODO: Catch other potential exception types here
        # TODO: Return actual object and status code in json (marshmallow?)
        return HttpStatuses.OK.value
