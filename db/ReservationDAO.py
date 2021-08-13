from db.AbstractDAO import AbstractDAO
from db.entities.Reservation import Reservation


class ReservationDAO(AbstractDAO):

    @staticmethod
    def get(reservation_id: int) -> Reservation:
        return (ReservationDAO.get_connection()
                .query(Reservation)
                .filter(Reservation.id == reservation_id)
                .one())

    @staticmethod
    def list() -> list[Reservation]:
        return [x for x in ReservationDAO.get_connection().query(Reservation).all()]
