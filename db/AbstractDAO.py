from abc import ABC

from sqlalchemy.orm import scoped_session

from db.ConnectionManager import ConnectionManager


class AbstractDAO(ABC):
    """
    Base class for DAOs. Needs to be extended for more complex handling of objects in the DB
    """
    @staticmethod
    def save(entity):
        """
        Generic implementation to save a given entity. Useful for creates/updates
        :param entity: SQLAlchemy entity
        """
        assert entity
        AbstractDAO.get_connection().add(entity)

    @staticmethod
    def delete(entity):
        """
        Generic implementation for the delete operation of a given entity
        :param entity: SQLAlchemy entity
        """
        assert entity
        AbstractDAO.get_connection().delete(entity)

    @staticmethod
    def generic_get(entity):
        """
        Generic implementation to fetch a single given entity with a matching id
        :param entity: SQLAlchemy entity with a valid id
        :return matching SQLAlchemy entity from the database
        """
        assert entity.id
        return (AbstractDAO.get_connection()
                .query(entity.__class__)
                .filter(entity.__class__.id == entity.id)
                .one())

    @staticmethod
    def begin():
        AbstractDAO.get_connection().begin()

    @staticmethod
    def rollback():
        AbstractDAO.get_connection().rollback()

    @staticmethod
    def commit():
        AbstractDAO.get_connection().commit()

    @staticmethod
    def flush():
        AbstractDAO.get_connection().flush()

    @staticmethod
    def get_connection() -> scoped_session:
        return ConnectionManager().get_session()
