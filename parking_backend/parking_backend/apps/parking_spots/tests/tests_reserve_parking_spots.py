from django.urls import reverse

from rest_framework import status
from rest_framework.test import force_authenticate

from freezegun import freeze_time

# Create your tests here.

from parking_backend.apps.parking_spots.views import (
    ReserveParkingSpotViewSet,
)

from parking_backend.apps.parking_spots.models import (
    ParkingUser,
)

from parking_backend.apps.parking_spots.helpers import ParkingTime
from .initial_test_setup import InitialTestSetup


class ReserveParkingSpotsTests(InitialTestSetup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = ReserveParkingSpotViewSet.as_view()

    def _run_test_case_and_return_http_status(
        self, reservation_date, parking_spot, username
    ):
        request_data = {
            "reservation_date": reservation_date,
            "parking_spot": parking_spot,
        }
        request = self.request_factory.post(
            reverse("reserve_parking_day"), request_data
        )
        username = username
        try:
            user = ParkingUser.objects.get(username=username)
            force_authenticate(request, user=user)
        except ParkingUser.DoesNotExist:
            pass  # User is not authenticated

        return self.view(request).status_code

    @freeze_time("2020-11-09 10:00:00")
    def test_unauthenticated_user_should_not_reserve_parking_spot(self):
        reservation_date = "2020-11-09"
        parking_spot = 3
        username = ""

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)

    @freeze_time("2020-11-09 10:00:00")
    def test_stephanie_should_not_reserve_not_existing_parking_spot(self):
        reservation_date = "2020-11-13"
        parking_spot = 101
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 10:00:00")
    def test_max_should_not_reserve_not_parking_spot_from_the_past(self):
        reservation_date = "2020-11-01"
        parking_spot = 1
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 10:00:00")
    def test_max_should_not_reserve_not_parking_spot_month_in_advance(self):
        reservation_date = "2020-12-09"
        parking_spot = 1
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 10:00:00")
    def test_stephanie_should_not_reserve_already_reserved_parking_spot(self):
        reservation_date = "2020-11-13"
        parking_spot = 1
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 10:00:00")
    def test_max_should_not_reserve_parking_spot_when_he_already_has_reservation_for_that_day(
        self,
    ):
        reservation_date = "2020-11-09"
        parking_spot = 5
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 10:00:00")
    def test_max_should_book_parking_space(self):
        reservation_date = "2020-11-11"
        parking_spot = 1
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)

    @freeze_time("2020-11-09 10:00:00")
    def test_admin_comany_A_should_not_book_parking_spot_company_B(self):
        reservation_date = "2020-11-11"
        parking_spot = 15
        username = "admin"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 10:00:00")
    def test_admin_comany_A_should_book_parking_spot_company_A(self):
        reservation_date = "2020-11-11"
        parking_spot = 10
        username = "admin"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)
