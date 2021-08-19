from datetime import datetime, timedelta

import pytest
import pytz

from api.entities.APIErrors import ReservationError
from api.service.ReservationService import ReservationService
from db.AbstractDAO import AbstractDAO
from db.GuestDAO import GuestDAO
from db.RoomDAO import RoomDAO
from db.entities.Guest import Guest
from db.entities.Room import Room
from test.app.TestAppBase import TestAppBase


class TestReservationService(TestAppBase):
    def test_creating_a_reservation(self):
        guest_id, room_id = self.__create_reservation_prerequisites()
        start_date = datetime.now(tz=pytz.utc) + timedelta(days=3)
        end_date = datetime.now(tz=pytz.utc) + timedelta(days=5)
        reservation_id = ReservationService.create(
            {
                "room_id": room_id,
                "guest_id": guest_id,
                "start_date": start_date.isoformat("T"),
                "end_date": end_date.isoformat("T"),
                "amount_of_guests": 1
            }
        )
        assert isinstance(reservation_id, int)
        assert reservation_id > 0

    def test_creating_a_conflicting_reservation(self):
        guest_id, room_id = self.__create_reservation_prerequisites()
        start_date = datetime.now(tz=pytz.utc) + timedelta(days=3)
        end_date = datetime.now(tz=pytz.utc) + timedelta(days=5)
        # Create a reservation
        reservation_id = ReservationService.create(
            {
                "room_id": room_id,
                "guest_id": guest_id,
                "start_date": start_date.isoformat("T"),
                "end_date": end_date.isoformat("T"),
                "amount_of_guests": 1
            }
        )

        start_date = datetime.now(tz=pytz.utc) + timedelta(days=4)
        end_date = datetime.now(tz=pytz.utc) + timedelta(days=5)
        # This reservation conflicts with the first one (same room, overlapping dates), so it should FAIL and throw
        # an error
        with pytest.raises(ReservationError):
            ReservationService.create(
                {
                    "room_id": room_id,
                    "guest_id": guest_id,
                    "start_date": start_date.isoformat("T"),
                    "end_date": end_date.isoformat("T"),
                    "amount_of_guests": 1
                }
            )

        start_date = datetime.now(tz=pytz.utc) + timedelta(days=6)
        end_date = datetime.now(tz=pytz.utc) + timedelta(days=7)
        # On the other hand, this next reservation dates should not conflict, and the creation should work with no
        # problems
        reservation_id2 = ReservationService.create(
            {
                "room_id": room_id,
                "guest_id": guest_id,
                "start_date": start_date.isoformat("T"),
                "end_date": end_date.isoformat("T"),
                "amount_of_guests": 1
            }
        )

        assert isinstance(reservation_id2, int)
        assert reservation_id2 > 0

    def __create_reservation_prerequisites(self) -> tuple[int, int]:
        """
        Creates a room and guest to be used for reservation purposes
        :return: returns the IDs of the created resources in a tuple. (guest_id, room_id)
        """
        room = Room()
        room.init_fields("Room 1", 2)
        guest = Guest()
        guest.init_fields("123", "Jorge", "Ocampo")

        AbstractDAO.begin()
        RoomDAO.save(room)
        GuestDAO.save(guest)
        AbstractDAO.commit()
        return guest.id, room.id
