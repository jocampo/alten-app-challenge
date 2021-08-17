import functools

from db.ReservationDAO import ReservationDAO
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
        return RoomDAO.get_all()

    @staticmethod
    def get_by_id(room_id: int) -> Room:
        """
        Fetches a single room given a matching id
        :param room_id: Id of the room being fetched
        :return: Room entity if found
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching room is found
        """
        assert isinstance(room_id, int), type(room_id)
        assert room_id > 0, room_id
        return RoomDAO.get(room_id)

    @staticmethod
    def create(create_request: dict) -> int:
        """
        Creates a room based on the specified create_request dict
        :param create_request: dictionary specifying the values for the room properties
        :return id of the newly created resource
        """
        assert isinstance(create_request, dict), type(create_request)
        assert len(create_request.keys()) > 0

        room = Room()
        set_field = functools.partial(setattr, room)
        for k, v in create_request.items():
            set_field(k, v)

        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.commit()
        return room.id

    @staticmethod
    def update(room_id: int, update_request: dict):
        """
        Updates a room based on the specified update_request dict
        :param room_id: Room id we want to update
        :param update_request: Fields we want to replace of the existing room
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching room is found for the update
        """
        assert isinstance(room_id, int), type(room_id)
        assert room_id > 0, room_id
        assert isinstance(update_request, dict), type(update_request)
        assert len(update_request.keys()) > 0

        room = RoomDAO.get(room_id)
        set_field = functools.partial(setattr, room)
        for k, v in update_request.items():
            set_field(k, v)

        RoomDAO.begin()
        RoomDAO.save(room)
        RoomDAO.commit()

    @staticmethod
    def delete(room_id: int):
        """
        Deletes a Room
        :param room_id: Room id that is to be deleted. If the room has reservations linked to it, those are all
        deleted beforehand as well
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching room is found for the deletion
        """
        assert isinstance(room_id, int), type(room_id)
        assert room_id > 0, room_id

        room = RoomDAO.get(room_id)
        linked_reservations = ReservationDAO.get_reservations_for_guest(room_id)

        RoomDAO.begin()
        for reservation in linked_reservations:
            ReservationDAO.delete(reservation)
        RoomDAO.delete(room)
        RoomDAO.commit()

