from ctypes import Union
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, BigInteger, Integer, Enum

from api.entities.ReservationStatus import ReservationStatus
from db.entities import Base
from sqlalchemy.ext.hybrid import hybrid_property

from utils.date_utils import DateUtils


class Reservation(Base):
    """
    Reservation SQLAlchemy entity
    """

    def init_fields(self, room_id: int, guest_id: int, start_date: datetime, end_date: datetime, amount_of_guests: int,
                    status: ReservationStatus):
        """
        Initializes the room entity with data
        :param room_id: id of the room tied to this reservation
        :param guest_id: id of the guest tied to this reservation
        :param start_date: starting date of the reservation
        :param end_date: end date of the reservation
        :param amount_of_guests: amount of guests to be included in the reservation
        :param status: status of the reservation
        """
        self.room_id = room_id
        self.guest_id = guest_id
        self.start_date = start_date
        self.end_date = end_date
        self.amount_of_guests = amount_of_guests
        self.status = status.value

    @hybrid_property
    def room_id(self) -> int:
        """
        Gets the id of the room in this reservation
        :return: id of the room entity
        """
        return self.__room_id

    @room_id.setter
    def room_id(self, room_id: int):
        """
        Sets the id of the room in this reservation
        :param room_id: id of the room in this reservation
        """
        assert isinstance(room_id, int), type(room_id)
        assert room_id > 0, room_id

        self.__room_id = room_id

    @hybrid_property
    def guest_id(self) -> int:
        """
        Gets the id of the guest in this reservation
        :return: id of the guest entity
        """
        return self.__guest_id

    @guest_id.setter
    def guest_id(self, guest_id: int):
        """
        Sets the id of the guest in this reservation
        :param guest_id: id of the guest in this reservation
        """
        assert isinstance(guest_id, int), type(guest_id)
        assert guest_id > 0, guest_id

        self.__guest_id = guest_id

    @hybrid_property
    def start_date(self) -> datetime:
        """
        Gets the starting datetime of the reservation
        :return: datetime indicating when the reservation starts
        """
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date: Union[datetime, str]):
        """
        Sets the starting datetime of the reservation
        :param start_date: datetime indicating when the reservation starts
        """
        assert isinstance(start_date, (datetime, str)), type(start_date)
        if isinstance(start_date, str):
            self.__start_date = DateUtils.convert_str_to_datetime(start_date)
        else:
            self.__start_date = start_date

    @hybrid_property
    def end_date(self) -> datetime:
        """
        Gets the end datetime of the reservation
        :return: datetime indicating when the reservation ends
        """
        return self.__end_date

    @end_date.setter
    def end_date(self, end_date: Union[datetime, str]):
        """
        Sets the end datetime of the reservation
        :param end_date: datetime indicating when the reservation ends
        """
        assert isinstance(end_date, (datetime, str)), type(end_date)
        if isinstance(end_date, str):
            self.__end_date = DateUtils.convert_str_to_datetime(end_date)
        else:
            self.__end_date = end_date

    @hybrid_property
    def amount_of_guests(self) -> int:
        """
        Gets the amount of guests in the reservation
        :return: Amount of guests in the reservation (i.e. 5)
        """
        return self.__amount_of_guests

    @amount_of_guests.setter
    def amount_of_guests(self, amount_of_guests: int):
        """
        Sets the amount of guests in the reservation
        :param amount_of_guests: a positive integer
        """
        assert isinstance(amount_of_guests, int), type(amount_of_guests)
        assert amount_of_guests > 0, amount_of_guests

        self.__amount_of_guests = amount_of_guests

    @hybrid_property
    def status(self) -> ReservationStatus:
        """
        Gets the status of the reservation
        :return: Status enum of the reservation (i.e. ReservationStatus.SCHEDULED)
        """
        return ReservationStatus(self.__status)

    @status.setter
    def status(self, status: ReservationStatus):
        """
        Sets the status of the reservation
        :param status: status of the reservation (i.e. ReservationStatus.SCHEDULED)
        """
        assert isinstance(status, ReservationStatus), type(status)

        self.__status = status.value

    __room_id = Column("room_id",
                       BigInteger,
                       ForeignKey(
                           "room.id",
                           name="fk_room_id",
                           onupdate="RESTRICT",
                           ondelete="RESTRICT"),
                       nullable=False)

    __guest_id = Column("guest_id",
                        BigInteger,
                        ForeignKey(
                            "guest.id",
                            name="fk_guest_id",
                            onupdate="RESTRICT",
                            ondelete="RESTRICT"),
                        nullable=False)

    __start_date = Column("start_date", DateTime(timezone=True), nullable=False)

    __end_date = Column("end_date", DateTime(timezone=True), nullable=False)

    __amount_of_guests = Column("amount_of_guests", Integer)

    __status = Column("status",
                      Enum(
                          "SCHEDULED",
                          "CANCELED",
                          name="reservation_status_type"),
                      nullable=False,
                      default="SCHEDULED")
