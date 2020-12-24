from django.urls import reverse

from rest_framework import status
from rest_framework.test import force_authenticate

# Create your tests here.

from parking_backend.apps.parking_spots.views import (
    RemoveReservationViewSet,
)

from parking_backend.apps.parking_spots.models import (
    ParkingUser,
    Reservation,
)

from parking_backend.apps.parking_spots.helpers import ParkingTime
from .initial_test_setup import InitialTestSetup


class RemoveReservationParkingSpotTests(InitialTestSetup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = RemoveReservationViewSet.as_view()

    def _run_test_case_and_return_http_status(self, reservation_id, username):
        remove_reservation_kwargs = {"pk": reservation_id}
        request = self.request_factory.delete(
            reverse("remove_reservation", kwargs={"pk": reservation_id})
        )
        username = username
        try:
            user = ParkingUser.objects.get(username=username)
            force_authenticate(request, user=user)
        except ParkingUser.DoesNotExist:
            pass  # User is not authenticated
        return self.view(request, **remove_reservation_kwargs).status_code

    def test_unauthenticated_user_should_not_remove_reservation(self):
        reservation_id = 1
        username = ""

        response_status = self._run_test_case_and_return_http_status(
            reservation_id=reservation_id,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)

    def test_max__should_not_remove_not_existing_reservation(self):
        reservation_id = 0
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_id=reservation_id,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_404_NOT_FOUND)

    def test_max_should_not_remove_adams_reservation(self):
        adams_reservation = Reservation.objects.filter(user__username="Adam")[0]
        reservation_id = adams_reservation.id
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_id=reservation_id,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_404_NOT_FOUND)

    def test_adam_should_remove_his_reservation(self):
        username = "Adam"
        adams_reservation = Reservation.objects.filter(user__username=username)[0]
        reservation_id = adams_reservation.id

        response_status = self._run_test_case_and_return_http_status(
            reservation_id=reservation_id,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_200_OK)
