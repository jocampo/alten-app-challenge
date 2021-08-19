from datetime import datetime

import pytz

from api.controllers.Routes import Routes
from api.controllers.guest.GuestFields import GuestFields
from api.entities.HttpStatuses import HttpStatuses
from db.GuestDAO import GuestDAO
from db.entities.Guest import Guest
from test.app.TestAppBase import TestAppBase


class TestGuestByIdController(TestAppBase):
    def test_get_guest__by_id(self):
        guest_id = self.__create_guest_data()
        request_uri = f"{Routes.GUESTS_BY_ID.value}".replace("<int:guest_id>", str(guest_id))
        response = self.client.get(request_uri)

        # Copy the response json so that we can modify it later
        response_dict = response.json.copy()

        # Test created_at / updated_at timestamps separately and then remove them from the response_dict,
        # since we can't compare an entire dict with those unpredictable values
        created_at = response.json[GuestFields.CREATED_AT.value]
        created_at_dt = datetime.fromisoformat(created_at)
        # Make sure it's a valid datetime str in iso format
        assert isinstance(created_at_dt, datetime)
        # and check that it has timezone info
        assert created_at_dt.tzinfo is not None

        updated_at = response.json[GuestFields.UPDATED_AT.value]
        assert updated_at is None

        del response_dict[GuestFields.CREATED_AT.value]
        del response_dict[GuestFields.UPDATED_AT.value]

        assert response_dict == {
            "id": guest_id,
            "document": "123",
            "first_name": "Jorge",
            "last_name": "Ocampo",
            "is_active": True
        }

    def test_update_guest(self):
        guest_id = self.__create_guest_data()
        request_uri = f"{Routes.GUESTS_BY_ID.value}".replace("<int:guest_id>", str(guest_id))
        response = self.client.put(
            request_uri, json={
                "is_active": False
            }
        )

        # We should get back the whole entity, but we only care about the updated field (is_active)
        assert response.json[GuestFields.IS_ACTIVE.value] is False
        # Now we check that the response dict has all the keys it should have
        assert all(x.value in response.json for x in GuestFields)

    def test_update_guest_bad_request(self):
        guest_id = self.__create_guest_data()
        request_uri = f"{Routes.GUESTS_BY_ID.value}".replace("<int:guest_id>", str(guest_id))

        # We're not allowed to set/update the updated_at field, since it's controlled by the server, so this should fail
        response = self.client.put(
            request_uri, json={
                "updated_at": datetime.now(tz=pytz.utc)
            }
        )
        assert response.status_code == HttpStatuses.BAD_REQUEST.value

    def test_update_guest_not_found(self):
        # We'll make a request to update a guest that doesn't exist in the DB, which should fail and get back to us
        # with a 404 NOT FOUND error
        request_uri = f"{Routes.GUESTS_BY_ID.value}".replace("<int:guest_id>", "25")

        # We're not allowed to set/update the updated_at field, since it's controlled by the server, so this should fail
        response = self.client.put(
            request_uri, json={
                "is_active": False
            }
        )
        assert response.status_code == HttpStatuses.NOT_FOUND.value

    def __create_guest_data(self) -> int:
        """
        Creates prerequisite data for the tests
        :return: returns the ID of the guest that was created
        """
        guest = Guest()
        guest.init_fields("123", "Jorge", "Ocampo")

        GuestDAO.begin()
        GuestDAO.save(guest)
        GuestDAO.commit()
        return guest.id