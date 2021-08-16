import functools

from db.ReservationDAO import ReservationDAO
from db.entities.Reservation import Reservation


class ReservationService:
    """
    Contains logic around the CRUD operations regarding the Reservation entity
    """
    @staticmethod
    def get_all() -> list[Reservation]:
        """
        Lists all reservations in the db, regardless of status
        :return: List of all reservations
        """
        return ReservationDAO.list()

    @staticmethod
    def get_by_id(reservation_id: int) -> Reservation:
        """
        Fetches a single reservation given a matching id
        :param reservation_id: Id of the reservation being fetched
        :return: Reservation entity if found
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching reservation is found
        """
        assert isinstance(reservation_id, int)
        assert reservation_id > 0
        return ReservationDAO.get(reservation_id)

    @staticmethod
    def create(create_request: dict):
        """
        Creates a reservation based on the specified create_request dict
        :param create_request: dictionary specifying the values for the reservation properties
        """
        assert isinstance(create_request, dict)
        assert len(create_request.keys()) > 0

        # TODO: Enforce ALL required fields, only
        # TODO: Business logic and validations re: reservations
        reservation = Reservation()
        set_field = functools.partial(setattr, reservation)
        for k, v in create_request.items():
            set_field(k, v)
            # TODO: confirm what happens if the dict contains keys that do not belong in a reservation entity

        ReservationDAO.begin()
        ReservationDAO.save(reservation)
        ReservationDAO.commit()

    @staticmethod
    def update(reservation_id: int, update_request: dict):
        """
        Updates a reservation based on the specified update_request dict
        :param reservation_id: Reservation id we want to update
        :param update_request: Fields we want to replace of the existing reservation
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching reservation is found for the update
        """
        assert isinstance(reservation_id, int)
        assert reservation_id > 0
        assert isinstance(update_request, dict)
        assert len(update_request.keys()) > 0

        # TODO: Business logic and validations re: reservations and times
        reservation = ReservationDAO.get(reservation_id)
        set_field = functools.partial(setattr, reservation)
        for k, v in update_request.items():
            set_field(k, v)
            # TODO: confirm what happens if the dict contains keys that do not belong in a reservation entity

        ReservationDAO.begin()
        ReservationDAO.save(reservation)
        ReservationDAO.commit()

    @staticmethod
    def delete(reservation_id: int):
        """
        Deletes a Reservation
        :param reservation_id: Reservation id that is to be deleted
        """
        assert isinstance(reservation_id, int)
        assert reservation_id > 0

        ReservationDAO.begin()
        ReservationDAO.delete(reservation_id)
        ReservationDAO.commit()

