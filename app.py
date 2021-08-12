import os
from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
from sqlalchemy import create_engine

from config import DATABASE_URL
os.environ["DATABASE_URL"] = DATABASE_URL

app = Flask(__name__)
heroku = Heroku(app)
CORS(app, support_credentials=True)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    app.run()
