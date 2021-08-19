import os
from unittest import mock

from alembic.command import downgrade, upgrade
from alembic.config import Config
from flask_testing import TestCase

from app import create_app
from db.AbstractDAO import AbstractDAO


@mock.patch.dict(os.environ, {"DATABASE_URL": "sqlite://"})
class TestAppBase(TestCase):
    """
    Base test class to inherit from in order to run tests related to the flask app/db.
    It mocks the OS environment variable DATABASE_URL to point towards an in-memory
    sqlite database for tests.
    """

    def create_app(self):
        """
        Essentially sets up the flask app
        """
        return create_app(True)

    def setUp(self):
        """
        To be ran before all tests
        """
        self.__alembic_cfg = Config("alembic.ini")
        # Run migrations all the way to head (all of them)
        upgrade(self.__alembic_cfg, "head")

    def tearDown(self):
        """
        Performs clean-up after every test case
        """
        # Remove the existing session
        AbstractDAO.get_connection().remove()
        # Cleanup all the db objects
        downgrade(self.__alembic_cfg, "base")
