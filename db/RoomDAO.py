from db.AbstractDAO import AbstractDAO
from db.entities.Room import Room


class RoomDAO(AbstractDAO):

    @staticmethod
    def get(room_id: int) -> Room:
        return (RoomDAO.get_connection()
                .query(Room)
                .filter(Room.id == room_id)
                .one())

    @staticmethod
    def list() -> list[Room]:
        return [x for x in RoomDAO.get_connection().query(Room).all()]
