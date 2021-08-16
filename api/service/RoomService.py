import functools

from db.RoomDAO import RoomDAO
from db.entities.Room import Room


class RoomService:
    """
    Contains logic around the CRUD operations regarding the Room entity
    """
    @staticmethod
    def get_all() -> list[Room]:
        """
        Lists all rooms in the db, regardless of status
        :return: List of all rooms
        """
        return RoomDAO.list()

    @staticmethod
    def get_by_id(room_id: int) -> Room:
        """
        Fetches a single room given a matching id
        :param room_id: Id of the room being fetched
        :return: Room entity if found
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching room is found
        """
        assert isinstance(room_id, int)
        assert room_id > 0
        return RoomDAO.get(room_id)

    @staticmethod
    def create(create_request: dict):
        """
        Creates a room based on the specified create_request dict
        :param create_request: dictionary specifying the values for the room properties
        """
        assert isinstance(create_request, dict)
        assert len(create_request.keys()) > 0

        room = Room()
        set_field = functools.partial(setattr, room)
        for k, v in create_request.items():
            set_field(k, v)
            # TODO: confirm what happens if the dict contains keys that do not belong in a room entity

        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.commit()

    @staticmethod
    def update(room_id: int, update_request: dict):
        """
        Updates a room based on the specified update_request dict
        :param room_id: Room id we want to update
        :param update_request: Fields we want to replace of the existing room
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching room is found for the update
        """
        assert isinstance(room_id, int)
        assert room_id > 0
        assert isinstance(update_request, dict)
        assert len(update_request.keys()) > 0

        room = RoomDAO.get(room_id)
        set_field = functools.partial(setattr, room)
        for k, v in update_request.items():
            set_field(k, v)
            # TODO: confirm what happens if the dict contains keys that do not belong in a room entity

        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.commit()

    @staticmethod
    def delete(room_id: int):
        """
        Deletes a Room
        TODO: should we look for reservations and delete them beforehand?
        :param room_id: Room id that is to be deleted
        """
        assert isinstance(room_id, int)
        assert room_id > 0

        RoomDAO.begin()
        RoomDAO.delete(room_id)
        RoomDAO.commit()

