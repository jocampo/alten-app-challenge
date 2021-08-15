from sqlalchemy import Column, String, Boolean, Integer
from dataclasses import dataclass

from sqlalchemy.ext.hybrid import hybrid_property

from db.entities import Base


@dataclass
class Room(Base):
    """
    Room SQLAlchemy entity
    """
    def init_fields(self, name, capacity, is_active=True):
        """
        Initializes the room entity with data
        :param name: a non-empty string that acts as name for the room (i.e. "Room 202")
        :param capacity: how many people fit in the room
        :param is_active: indicates if the room is active or not
        """
        self.name = name
        self.capacity = capacity
        self.is_active = is_active

    @hybrid_property
    def name(self) -> str:
        """
        Gets the name of the room
        :return: Name of the Room (i.e. "Room 202")
        """
        return self.__name

    @name.setter
    def name(self, name: str):
        """
        Sets the name of the room
        :param name: a non-empty name of the room
        """
        assert isinstance(name, str)
        assert name

        self.__name = name

    @hybrid_property
    def capacity(self) -> int:
        """
        Gets the capacity of the room
        :return: Capacity of the room (i.e. 5)
        """
        return self.__capacity

    @capacity.setter
    def capacity(self, capacity: int):
        """
        Sets the capacity of the room
        :param capacity: a positive integer
        """
        assert isinstance(capacity, int)
        assert capacity > 0

        self.__capacity = capacity

    @hybrid_property
    def is_active(self) -> bool:
        """
        Indicates if the room is active or not
        :return: boolean indicating the status of the room
        """
        return self.__is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        """
        Sets whether a room is active or not
        :param is_active: a boolean indicating if the room is active or not
        """
        assert isinstance(is_active, bool)
        self.__is_active = is_active

    __name = Column("name", String, nullable=False)

    __capacity = Column("capacity", Integer)

    __is_active = Column("is_active", Boolean, nullable=False, default=True)
