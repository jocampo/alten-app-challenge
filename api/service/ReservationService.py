import functools
from datetime import datetime

from api.entities.APIErrors import ReservationError
from api.entities.ReservationStatus import ReservationStatus
from api.service.GuestService import GuestService
from api.service.RoomService import RoomService
from db.ReservationDAO import ReservationDAO
from db.entities.Reservation import Reservation
from utils.DateUtils import DateUtils


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
        return ReservationDAO.get_all()

    @staticmethod
    def get_by_id(reservation_id: int) -> Reservation:
        """
        Fetches a single reservation given a matching id
        :param reservation_id: Id of the reservation being fetched
        :return: Reservation entity if found
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching reservation is found
        """
        assert isinstance(reservation_id, int), type(reservation_id)
        assert reservation_id > 0, reservation_id
        return ReservationDAO.get(reservation_id)

    @staticmethod
    def create(create_request: dict) -> int:
        """
        Creates a reservation based on the specified create_request dict
        :param create_request: dictionary specifying the values for the reservation properties
        :return id of the newly created resource
        :raise ReservationError: if any business logic issues are found with the creation request, this error is raised
        with a relevant description of the error so that the caller can take action.
        """
        assert isinstance(create_request, dict), type(create_request)
        assert len(create_request.keys()) > 0

        reservation = Reservation()
        set_field = functools.partial(setattr, reservation)
        for k, v in create_request.items():
            set_field(k, v)

        booking_error_message = ""

        # Validate that the stay isn't longer than X days
        stay_duration = reservation.end_date - reservation.start_date
        if stay_duration.days > ReservationService.__MAX_STAY_DAYS:
            booking_error_message = f"Your reservation exceeds the max allowed stay duration of " \
                                    f"{ReservationService.__MAX_STAY_DAYS} day(s)"

        # Validate that the stay isn't shorter than X days
        if stay_duration.days <= ReservationService.__MIN_STAY_DAYS:
            booking_error_message = f"Your reservation must be at least " \
                                    f"{ReservationService.__MIN_STAY_DAYS} day(s) long"

        time_until_reservation_starts = reservation.start_date - datetime.now()
        # Validate that the reservation starts in at least X days
        if time_until_reservation_starts.days < ReservationService.__MIN_DAYS_BEFORE_RESERVATION_START:
            booking_error_message = f"Your reservation must start at least " \
                                    f"{ReservationService.__MIN_DAYS_BEFORE_RESERVATION_START} day(s) from now"

        # Validate that the reservation isn't made with more than X days in advance
        if time_until_reservation_starts.days > ReservationService.__MAX_DAYS_IN_ADVANCE:
            booking_error_message = f"Your reservation can't be booked with more than " \
                                    f"{ReservationService.__MAX_DAYS_IN_ADVANCE} day(s) of anticipation"

        # Validate that the room being reserved is active
        room = RoomService.get_by_id(reservation.room_id)
        if not room.is_active:
            booking_error_message = f"The room you're attempting to reserve (room_id: {reservation.room_id}) is NOT " \
                                    f"active"

        # Validate that the guest trying to make the reservation is active
        guest = GuestService.get_by_id(reservation.guest_id)
        if not guest.is_active:
            booking_error_message = f"The guest attempting to make the reservation (guest_id: {reservation.guest_id})" \
                                    f" is NOT active"

        # Validate that the room being reserved doesn't have any SCHEDULED reservations that overlap
        if not ReservationService.check_room_availability(
                reservation.guest_id, reservation.start_date, reservation.end_date
        ):
            booking_error_message = f"The room you're attempting to reserve (room_id: {reservation.room_id}) is not " \
                                    f"available between the specified start_date and end_date. Please change them and" \
                                    f" try again."

        if booking_error_message:
            raise ReservationError(booking_error_message)

        ReservationDAO.begin()
        ReservationDAO.save(reservation)
        ReservationDAO.commit()
        return reservation.id

    @staticmethod
    def update(reservation_id: int, update_request: dict):
        """
        Updates a reservation based on the specified update_request dict
        :param reservation_id: Reservation id we want to update
        :param update_request: Fields we want to replace of the existing reservation
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching reservation is found for the update
        """
        assert isinstance(reservation_id, int), type(reservation_id)
        assert reservation_id > 0, reservation_id
        assert isinstance(update_request, dict), type(update_request)
        assert len(update_request.keys()) > 0

        # TODO: Business logic and validations re: reservations and times
        reservation = ReservationDAO.get(reservation_id)
        set_field = functools.partial(setattr, reservation)
        for k, v in update_request.items():
            set_field(k, v)

        ReservationDAO.begin()
        ReservationDAO.save(reservation)
        ReservationDAO.commit()

    @staticmethod
    def delete(reservation_id: int):
        """
        Deletes a Reservation
        :param reservation_id: Reservation id that is to be deleted
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching reservation is found for the update
        """
        assert isinstance(reservation_id, int), type(reservation_id)
        assert reservation_id > 0, reservation_id

        reservation = ReservationDAO.get(reservation_id)
        ReservationDAO.begin()
        ReservationDAO.delete(reservation)
        ReservationDAO.commit()

    @staticmethod
    def check_room_availability(room_id: int, start_date: datetime, end_date: datetime) -> bool:
        """
        Checks if a given room_id is available between start_date and end_date.
        This method checks for reservations with status L{ReservationStatus.SCHEDULED}
        that belong to this room. If any of them overlap with the desired start/end dates,
        we return C{False}. Otherwise, we return C{True}.

        :param room_id: Room we're going to check the availability for
        :param start_date: start_date of the desired reservation we're going to check the availability for
        :param end_date: end_date of the desired reservation we're going to check the availability for
        :return: C{False} if at least 1 reservation of this room overlaps with the desired start/end dates.
        Otherwise, C{True} is returned.
        """
        # Grab all SCHEDULED reservations (namely, weed out the CANCELED ones) for the desired room_id
        reservations = [x for x in ReservationService.get_all() if
                        x.status is ReservationStatus.SCHEDULED and
                        x.room_id == room_id]

        for reservation in reservations:
            if DateUtils.check_if_date_ranges_overlap(
                    start_date, end_date, reservation.start_date, reservation.end_date
            ):
                return False

        return True

    """ Min stay for reservations (measured in days) """
    __MIN_STAY_DAYS = 1

    """ Max stay for reservations (measured in days) """
    __MAX_STAY_DAYS = 3

    """ Max number of days in advance with which a reservation can be made"""
    __MAX_DAYS_IN_ADVANCE = 30

    """ Min number of days that has to exist between the reservation start_date and the time of the request """
    __MIN_DAYS_BEFORE_RESERVATION_START = 1
