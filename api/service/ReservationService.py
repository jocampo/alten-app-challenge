import functools
from datetime import datetime

from pytz import utc

from api.controllers.reservation.ReservationFields import ReservationFields
from api.entities.APIErrors import ReservationError
from api.entities.ErrorMessages import ErrorMessages
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

        # Check that start_date and end_date have tz info. Otherwise, reject the request
        if reservation.start_date.tzinfo is None or reservation.end_date.tzinfo is None:
            raise ReservationError(ErrorMessages.TIMEZONE_MISSING_FROM_DATE_FIELDS.value)

        # Start performing some validations for the reservation
        ReservationService.__validate_reservation_dates(reservation)
        ReservationService.__validate_room_and_guest(reservation)
        ReservationService.__validate_reservation_scheduling_conflicts(reservation)

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
        :raise ReservationError: if any business logic issues are found with the update request, this error is raised
        with a relevant description of the error so that the caller can take action.
        """
        assert isinstance(reservation_id, int), type(reservation_id)
        assert reservation_id > 0, reservation_id
        assert isinstance(update_request, dict), type(update_request)
        assert len(update_request.keys()) > 0

        reservation = ReservationDAO.get(reservation_id)
        set_field = functools.partial(setattr, reservation)
        for k, v in update_request.items():
            set_field(k, v)

        # Check that start_date and end_date have tz info. Otherwise, reject the request
        if reservation.start_date.tzinfo is None or reservation.end_date.tzinfo is None:
            raise ReservationError(ErrorMessages.TIMEZONE_MISSING_FROM_DATE_FIELDS.value)

        # Start performing some validations for the reservation
        ReservationService.__validate_room_and_guest(reservation)

        # If any of these fields are included in the update request AND the room has a status of
        # C{ReservationStatus.SCHEDULED}, we have to do some checks for the dates
        if (ReservationFields.ROOM_ID.value in update_request or
            ReservationFields.STATUS.value in update_request or
            ReservationFields.START_DATE.value in update_request or
            ReservationFields.END_DATE.value in update_request) and \
                reservation.status is ReservationStatus.SCHEDULED:

            ReservationService.__validate_reservation_dates(reservation)
            ReservationService.__validate_reservation_scheduling_conflicts(reservation)

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
    def check_room_availability(room_id: int, start_date: datetime, end_date: datetime,
                                reservation_id: int = None) -> bool:
        """
        Checks if a given room_id is available between start_date and end_date.
        This method checks for reservations with status C{ReservationStatus.SCHEDULED}
        that belong to this room. If any of them overlap with the desired start/end dates,
        we return C{False}. Otherwise, we return C{True}.

        :param room_id: Room we're going to check the availability for
        :param start_date: start_date of the desired reservation we're going to check the availability for
        :param end_date: end_date of the desired reservation we're going to check the availability for
        :param reservation_id: if included, that reservation is taken out of consideration in the availability check
        :return: C{False} if at least 1 reservation of this room overlaps with the desired start/end dates.
        Otherwise, C{True} is returned.
        """
        # Grab all SCHEDULED reservations (namely, weed out the CANCELED ones) for the desired room_id
        reservations = [x for x in ReservationService.get_all() if
                        x.status is ReservationStatus.SCHEDULED and
                        x.room_id == room_id]

        # If this parameter is defined, we want to remove that Reservation from the list of potential conflicting
        # reservations
        if reservation_id:
            reservations = [x for x in reservations if x.id != reservation_id]

        for reservation in reservations:
            if DateUtils.check_if_date_ranges_overlap(
                    start_date, end_date, reservation.start_date, reservation.end_date
            ):
                return False

        return True

    @staticmethod
    def __validate_reservation_scheduling_conflicts(reservation: Reservation):
        """
        Performs validations upon the reservation related to prevent scheduling conflicts with other qualifying
        reservations.

        :param reservation: Reservation entity to make the validations upon
        :raise ReservationError: if any business logic issues are found with the reservation, this error is raised
        with a relevant description of the error so that the caller can take action.
        """
        if not ReservationService.check_room_availability(
                reservation.room_id, reservation.start_date, reservation.end_date, reservation.id
        ):
            raise ReservationError(
                f"The room you're attempting to reserve (room_id: {reservation.room_id}) is not available between the "
                f"specified start_date and end_date. Please change them and try again."
            )

    @staticmethod
    def __validate_room_and_guest(reservation: Reservation):
        """
        Performs validations upon the reservation related to the guest_id, room_id and amount_of_guests to make sure
        that they comply with the desired business logic

        :param reservation: Reservation entity to make the validations upon
        :raise ReservationError: if any business logic issues are found with the reservation, this error is raised
        with a relevant description of the error so that the caller can take action.
        """
        booking_error_message = ""

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

        # Check that the room can hold the amount of guests in the reservation
        if reservation.amount_of_guests and room.capacity and reservation.amount_of_guests > room.capacity:
            booking_error_message = f"The room you're trying to reserve (room_id: {reservation.room_id})  is too " \
                                    f"small, it can only hold {room.capacity} guest(s)"

        if booking_error_message:
            raise ReservationError(booking_error_message)

    @staticmethod
    def __validate_reservation_dates(reservation: Reservation):
        """
        Performs validations upon the reservation related to the start_date and end_date to make sure that they comply
        with the desired business logic

        :param reservation: Reservation entity to make the validations upon
        :raise ReservationError: if any business logic issues are found with the reservation, this error is raised
        with a relevant description of the error so that the caller can take action.
        """
        booking_error_message = ""

        # Validate that the stay isn't longer than X days
        stay_duration = reservation.end_date - reservation.start_date
        if stay_duration.days > ReservationService.__MAX_STAY_DAYS:
            booking_error_message = f"Your reservation exceeds the max allowed stay duration of " \
                                    f"{ReservationService.__MAX_STAY_DAYS} day(s)"
        # Validate that the stay isn't shorter than X days
        if stay_duration.days < ReservationService.__MIN_STAY_DAYS:
            booking_error_message = f"Your reservation must be at least " \
                                    f"{ReservationService.__MIN_STAY_DAYS} day(s) long"

        time_until_reservation_starts = reservation.start_date - datetime.now(utc)
        # Validate that the reservation starts in at least X days
        if time_until_reservation_starts.days < ReservationService.__MIN_DAYS_BEFORE_RESERVATION_START:
            booking_error_message = f"Your reservation must start at least " \
                                    f"{ReservationService.__MIN_DAYS_BEFORE_RESERVATION_START} day(s) from now"

        # Validate that the reservation isn't made with more than X days in advance
        if time_until_reservation_starts.days > ReservationService.__MAX_DAYS_IN_ADVANCE:
            booking_error_message = f"Your reservation can't be booked with more than " \
                                    f"{ReservationService.__MAX_DAYS_IN_ADVANCE} day(s) of anticipation"

        if booking_error_message:
            raise ReservationError(booking_error_message)

    """ Min stay for reservations (measured in days) """
    __MIN_STAY_DAYS = 1

    """ Max stay for reservations (measured in days) """
    __MAX_STAY_DAYS = 3

    """ Max number of days in advance with which a reservation can be made"""
    __MAX_DAYS_IN_ADVANCE = 30

    """ Min number of days that has to exist between the reservation start_date and the time of the request """
    __MIN_DAYS_BEFORE_RESERVATION_START = 1
