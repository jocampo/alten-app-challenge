import os
from unittest import mock

from alembic.command import downgrade, upgrade
from alembic.config import Config
from flask_testing import TestCase

from app import create_app


class TestAppBase(TestCase):

    @mock.patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"})
    def create_app(self):
        return create_app(True)

    @mock.patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"})
    def setUp(self):
        self.__alembic_cfg = Config("alembic.ini")
        upgrade(self.__alembic_cfg, "head")

    @mock.patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:"})
    def tearDown(self):
        downgrade(self.__alembic_cfg, "base")
