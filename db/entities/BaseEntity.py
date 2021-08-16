from datetime import datetime

from sqlalchemy.orm import declared_attr
from sqlalchemy.schema import Column
from sqlalchemy.sql import func
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.ext.hybrid import hybrid_property


class BaseEntity:
    """
    Base Entity to serve as declarative base for other SQLAlchemy entities
    """
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Prevents us from having to set this on every SQLAlchemy entity
        :return: tablename taken from the class name
        """
        return cls.__name__.lower()

    @hybrid_property
    def id(self) -> int:
        """
        Gets the id of the entity
        :return: id of the entity
        """
        return self.__id

    @id.setter
    def id(self, id: int):
        """
        Sets the id of the entity
        :param id: identifier of the entity
        """
        assert isinstance(id, int), type(id)
        assert id > 0, id

        self.__id = id

    @hybrid_property
    def created_at(self) -> datetime:
        """
        Gets the created_at datetime
        :return: datetime indicating when the entity was created
        """
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        """
        Sets the created_at datetime of the entity
        :param created_at: datetime indicating when the entity was created
        """
        assert isinstance(created_at, datetime), type(created_at)
        self.__created_at = created_at

    @hybrid_property
    def updated_at(self) -> datetime:
        """
        Gets the updated_at datetime
        :return: datetime indicating when the entity was updated
        """
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        """
        Sets the updated_at datetime of the entity
        :param updated_at: datetime indicating when the entity was updated
        """
        assert isinstance(updated_at, datetime), type(updated_at)
        self.__updated_at = updated_at

    __id = Column("id", Integer, primary_key=True)

    __created_at = Column("created_at", DateTime(timezone=True), server_default=func.now())

    __updated_at = Column("updated_at", DateTime(timezone=True), onupdate=func.now())
