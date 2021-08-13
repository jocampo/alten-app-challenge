import os
from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine

from config import DATABASE_URL
from db.AbstractDAO import AbstractDAO
from db.ConnectionManager import ConnectionManager
from db.GuestDAO import GuestDAO
from db.entities.Guest import Guest
from db.entities.Room import Room
from utils.heroku import HerokuUtils

if "DATABASE_URL" in os.environ:
    db_url = HerokuUtils.parse_postgres_dialect(os.environ['DATABASE_URL'])
    # os.environ['DATABASE_URL'] = db_url
else:
    os.environ["DATABASE_URL"] = DATABASE_URL
    db_url = DATABASE_URL

app = Flask(__name__)
heroku = Heroku(app)
CORS(app, support_credentials=True)

connection_manager = ConnectionManager(db_url)
session = flask_scoped_session(connection_manager.get_session_factory(), app)


@app.route('/')
def hello_world():
    guest = Guest("222222", "Pepe", "Suarez")
    GuestDAO.begin()
    GuestDAO.save(guest)
    GuestDAO.commit()
    return 'Hello World!'


if __name__ == "__main__":
    app.run()
