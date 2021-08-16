import os
from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from flask_restful import Api
from flask_sqlalchemy_session import flask_scoped_session

from api.controllers.guest.GuestByIdController import GuestByIdController
from api.controllers.guest.GuestController import GuestController
from api.controllers.Routes import Routes
from config import DATABASE_URL
from db.ConnectionManager import ConnectionManager
from utils.heroku import HerokuUtils

if "DATABASE_URL" in os.environ:
    db_url = HerokuUtils.parse_postgres_dialect(os.environ["DATABASE_URL"])
else:
    os.environ["DATABASE_URL"] = DATABASE_URL
    db_url = DATABASE_URL

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(app)
heroku = Heroku(app)
CORS(app, support_credentials=True)

connection_manager = ConnectionManager(db_url)
session = flask_scoped_session(connection_manager.get_session_factory(), app)


@app.route("/")
def index():
    return "Welcome to the Hotel API"


api.add_resource(GuestController, Routes.GUESTS.value)
api.add_resource(GuestByIdController, Routes.GUESTS_BY_ID.value)

if __name__ == "__main__":
    app.run()
