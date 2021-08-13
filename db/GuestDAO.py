from db.AbstractDAO import AbstractDAO
from db.entities.Guest import Guest


class GuestDAO(AbstractDAO):

    @staticmethod
    def get(guest_id: int) -> Guest:
        return (GuestDAO.get_connection()
                .query(Guest)
                .filter(Guest.id == guest_id)
                .one())

    @staticmethod
    def list() -> list[Guest]:
        return [x for x in GuestDAO.get_connection().query(Guest).all()]
