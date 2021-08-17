from sqlalchemy import Column, String, Boolean
from dataclasses import dataclass

from db.entities import Base

from sqlalchemy.ext.hybrid import hybrid_property


@dataclass
class Guest(Base):
    """
    Guest SQLAlchemy entity
    """
    document: str
    first_name: str
    last_name: str
    is_active: bool

    def init_fields(self, document: str, first_name: str, last_name: str, is_active: bool = True):
        """
        Initializes the guest entity with data
        """
        self.document = document
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active

    @hybrid_property
    def document(self) -> str:
        """
        Document Number (i.e. national ID or passport) of the guest
        :return: string representation of the guest's Document Number
        """
        return self.__document

    @document.setter
    def document(self, document: str):
        """
        Sets the Document Number (i.e. national ID or passport) for the guest
        :param document: Document Number (i.e. national ID or passport) of the guest
        """
        assert isinstance(document, str), type(document)
        assert document, document
        self.__document = document

    @hybrid_property
    def first_name(self) -> str:
        """
        First name of the guest
        :return: first name of the guest as a string
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: str):
        """
        Sets the first name for the guest
        :param first_name: first name of the guest
        """
        assert isinstance(first_name, str), type(first_name)
        assert first_name, first_name
        self.__first_name = first_name

    @hybrid_property
    def last_name(self) -> str:
        """
        Last name of the guest
        :return: last name of the guest as a string
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: str):
        """
        Sets the last name for the guest
        :param last_name: last name of the guest
        """
        assert isinstance(last_name, str), type(last_name)
        assert last_name, last_name
        self.__last_name = last_name

    @hybrid_property
    def is_active(self) -> bool:
        """
        Indicates if the guest is active or not
        :return: boolean indicating the status of the guest
        """
        return self.__is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        """
        Sets whether a guest is active or not
        :param is_active: a boolean indicating if the guest entity is active or not
        """
        assert isinstance(is_active, bool), type(is_active)
        self.__is_active = is_active

    __document = Column("document", String, nullable=False)

    __first_name = Column("first_name", String, nullable=False)

    __last_name = Column("last_name", String, nullable=False)

    __is_active = Column("is_active", Boolean, nullable=False, default=True)
