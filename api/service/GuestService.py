import functools

from db.GuestDAO import GuestDAO
from db.entities.Guest import Guest


class GuestService:
    """
    Contains logic around the CRUD operations regarding the Guest entity
    """
    @staticmethod
    def get_all() -> list[Guest]:
        """
        Lists all guests in the db, regardless of status
        :return: List of all guests
        """
        return GuestDAO.list()

    @staticmethod
    def get_by_id(guest_id: int) -> Guest:
        """
        Fetches a single guest given a matching id
        :param guest_id: Id of the guest being fetched
        :return: Guest entity if found
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching guest is found
        """
        assert isinstance(guest_id, int), type(guest_id)
        assert guest_id > 0
        return GuestDAO.get(guest_id)

    @staticmethod
    def create(create_request: dict) -> int:
        """
        Creates a guest based on the specified create_request dict
        :param create_request: dictionary specifying the values for the guest properties
        :return id of the newly created resource
        """
        assert isinstance(create_request, dict), type(create_request)
        assert len(create_request.keys()) > 0

        guest = Guest()
        set_field = functools.partial(setattr, guest)
        for k, v in create_request.items():
            set_field(k, v)

        GuestDAO.begin()
        GuestDAO.save(guest)
        GuestDAO.commit()
        return guest.id

    @staticmethod
    def update(guest_id: int, update_request: dict):
        """
        Updates a guest based on the specified update_request dict
        :param guest_id: Guest id we want to update
        :param update_request: Fields we want to replace of the existing guest
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching guest is found for the update
        """
        assert isinstance(guest_id, int), type(guest_id)
        assert guest_id > 0, guest_id
        assert isinstance(update_request, dict), type(update_request)
        assert len(update_request.keys()) > 0

        guest = GuestDAO.get(guest_id)
        set_field = functools.partial(setattr, guest)
        for k, v in update_request.items():
            set_field(k, v)

        GuestDAO.begin()
        GuestDAO.save(guest)
        GuestDAO.commit()

    @staticmethod
    def delete(guest_id: int):
        """
        Deletes a Guest that matches the provided guest_id
        TODO: should we look for reservations and delete them beforehand?
        :param guest_id: Guest id that is to be deleted
        :raises sqlalchemy.orm.exc.NoResultFound: when no matching guest is found for the deletion
        """
        assert isinstance(guest_id, int), type(guest_id)
        assert guest_id > 0, guest_id

        guest = GuestDAO.get(guest_id)
        GuestDAO.begin()
        GuestDAO.delete(guest)
        GuestDAO.commit()

