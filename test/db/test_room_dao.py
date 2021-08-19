from db.RoomDAO import RoomDAO
from db.entities.Room import Room
from test.app.TestAppBase import TestAppBase


class TestRoomDAO(TestAppBase):
    def test_creating_a_room(self):
        room = Room()
        room.name = "Roomie"
        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.commit()

        assert room.id is not None

    def test_fetching_a_room(self):
        room = Room()
        room.name = "Roomie"
        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.commit()

        same_room = RoomDAO.get(room.id)
        assert room is same_room

    def test_listing_rooms(self):
        room = Room()
        room.name = "Roomie"
        room2 = Room()
        room2.name = "Roomie2"

        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.save(room2)
        RoomDAO.commit()

        rooms = RoomDAO.get_all()
        assert len(rooms) == 2

    def test_deleting_a_room(self):
        room = Room()
        room.name = "Roomie"

        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.commit()

        RoomDAO.begin()
        RoomDAO.delete(room)
        RoomDAO.commit()

        rooms = RoomDAO.get_all()
        assert len(rooms) == 0
