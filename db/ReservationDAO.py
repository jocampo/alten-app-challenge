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
    def get_all() -> list[Reservation]:
        return [x for x in ReservationDAO.get_connection().query(Reservation).all()]

    @staticmethod
    def get_reservations_for_guest(guest_id: int) -> list[Reservation]:
        """
        Gets all the reservations where the guest_id matches that of the reservation
        :param guest_id: guest_id to look for in the reservations
        :return: list of matching Reservations
        """
        return [x for x in ReservationDAO.get_connection().query(Reservation).filter(Reservation.guest_id == guest_id)]

    @staticmethod
    def get_reservations_for_room(room_id: int) -> list[Reservation]:
        """
        Gets all the reservations where the guest_id matches that of the reservation
        :param room_id: guest_id to look for in the reservations
        :return: list of matching Reservations
        """
        return [x for x in ReservationDAO.get_connection().query(Reservation).filter(Reservation.room_id == room_id)]
