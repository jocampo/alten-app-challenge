from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from flask_sqlalchemy_session import current_session
from utils.singleton import Singleton


class ConnectionManager(metaclass=Singleton):
    """
    Singleton class that creates the engine and session factory once for the DB. On future calls,
    the original objects will be used.
    """
    def __init__(self, database_url=None):
        """
        Creates the engine and the session maker to be used for future connections
        :param database_url:
        """
        assert database_url

        engine = create_engine(database_url)
        self.__engine = engine
        self.__session_factory = sessionmaker(bind=engine, autocommit=True)

    def get_session_factory(self) -> sessionmaker:
        """
        Returns the session factory originally initialized when the engine was created
        :return: sessionmaker object
        """
        return self.__session_factory

    def get_session(self) -> scoped_session:
        """
        If a session is already defined (by the current request), return it. Otherwise, create a new one
        :return: Scoped session depending on the context
        """
        if current_session:
            return current_session
        return scoped_session(self.__session_factory)
