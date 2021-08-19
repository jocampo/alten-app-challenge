import os

from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from flask_restful import Api
from flask_sqlalchemy_session import flask_scoped_session

from config import DATABASE_URL
from config.JSONEncoder import CustomJSONEncoder
from config.SwaggerConfig import SWAGGERUI_BLUEPRINT
from db.ConnectionManager import ConnectionManager
from utils.HerokuUtils import HerokuUtils


def create_app(is_testing_context: bool = False):
    if "DATABASE_URL" in os.environ:
        db_url = HerokuUtils.parse_postgres_dialect(os.environ["DATABASE_URL"])
    else:
        os.environ["DATABASE_URL"] = DATABASE_URL
        db_url = DATABASE_URL

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.json_encoder = CustomJSONEncoder

    if is_testing_context:
        app.config["TESTING"] = True

    from api.controllers.Routes import Routes
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=Routes.SWAGGER.value)

    api = Api(app)
    heroku = Heroku(app)
    CORS(app, support_credentials=True)

    connection_manager = ConnectionManager(db_url)
    session = flask_scoped_session(connection_manager.get_session_factory(), app)

    @app.route("/")
    def index():
        return "Welcome to the Hotel API"

    # Register routes for the API, binding a controller to each route
    from api.controllers.custom.RoomAvailabilityController import RoomAvailabilityController
    from api.controllers.guest.GuestByIdController import GuestByIdController
    from api.controllers.guest.GuestController import GuestController
    from api.controllers.reservation.ReservationByIdController import ReservationByIdController
    from api.controllers.reservation.ReservationController import ReservationController
    from api.controllers.room.RoomByIdController import RoomByIdController
    from api.controllers.room.RoomController import RoomController

    api.add_resource(GuestController, Routes.GUESTS.value)
    api.add_resource(GuestByIdController, Routes.GUESTS_BY_ID.value)
    api.add_resource(RoomController, Routes.ROOMS.value)
    api.add_resource(RoomByIdController, Routes.ROOMS_BY_ID.value)
    api.add_resource(ReservationController, Routes.RESERVATIONS.value)
    api.add_resource(ReservationByIdController, Routes.RESERVATIONS_BY_ID.value)
    api.add_resource(RoomAvailabilityController, Routes.ROOM_AVAILABILITY.value)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
