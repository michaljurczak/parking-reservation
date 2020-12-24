from rest_framework import status
from rest_framework.test import force_authenticate

from freezegun import freeze_time

from django.urls import reverse

# Create your tests here.

from parking_backend.apps.parking_spots.views import (
    PeriodReserveParkingSpotViewSet,
)

from parking_backend.apps.parking_spots.models import (
    ParkingUser,
)

from parking_backend.apps.parking_spots.helpers import ParkingTime
from .initial_test_setup import InitialTestSetup


class ReservePeriodParkingSpotsTests(InitialTestSetup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = PeriodReserveParkingSpotViewSet.as_view()

    def _run_test_case_and_return_http_status(
        self,
        reservation_date,
        parking_spot,
        start_reservation_time,
        end_reservation_time,
        username,
    ):
        request_data = {
            "reservation_date": reservation_date,
            "parking_spot": parking_spot,
            "start_reservation_time": start_reservation_time,
            "end_reservation_time": end_reservation_time,
        }
        request = self.request_factory.post(
            reverse("reserve_parking_time"), request_data
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
        start_reservation_time = "15:00"
        end_reservation_time = "15:10"
        username = ""

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)

    @freeze_time("2020-11-09 10:00:00")
    def test_stephanie_should_book_parking_spot_for_10_minutes(self):
        reservation_date = "2020-11-12"
        parking_spot = 3
        start_reservation_time = "12:00"
        end_reservation_time = "12:10"
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)

    @freeze_time("2020-11-09 10:00:00")
    def test_stephanie_should_not_book_parking_spot_when_starting_time_is_in_the_past(
        self,
    ):
        reservation_date = "2020-11-09"
        parking_spot = 3
        start_reservation_time = "09:50"
        end_reservation_time = "12:10"
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_stephanie_should_not_book_parking_spot_when_booking_period_is_less_than_default_10_min(
        self,
    ):
        reservation_date = "2020-11-09"
        parking_spot = 3
        start_reservation_time = "13:00"
        end_reservation_time = "13:05"
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_book_parking_spot_for_20_minutes(self):
        reservation_date = "2020-11-09"
        parking_spot = 3
        start_reservation_time = "13:00"
        end_reservation_time = "13:20"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)

    @freeze_time("2020-11-09 13:00:00")
    def test_stephanie_should_book_parking_spot_for_all_day(self):
        reservation_date = "2020-11-11"
        parking_spot = 3
        start_reservation_time = "00:00"
        end_reservation_time = "23:59"
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)

    @freeze_time("2020-11-09 13:00:00")
    def test_adam_should_not_book_parking_spot_when_he_already_has_reservation_for_that_day(
        self,
    ):
        reservation_date = "2020-11-13"
        parking_spot = 4
        start_reservation_time = "10:00"
        end_reservation_time = "11:00"
        username = "Adam"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_not_book_parking_spot_for_tomorrow_when_he_already_has_reservation_for_tomorrow(
        self,
    ):
        reservation_date = "2020-11-10"
        parking_spot = 4
        start_reservation_time = "22:00"
        end_reservation_time = "23:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 06:00:00")
    def test_max_should_not_book_parking_spot_for_later_today_when_his_reservation_for_today_has_not_finished_yet(
        self,
    ):
        reservation_date = "2020-11-09"
        parking_spot = 4
        start_reservation_time = "18:00"
        end_reservation_time = "19:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_book_parking_spot_for_later_today_when_his_reservation_for_today_has_finished(
        self,
    ):
        reservation_date = "2020-11-09"
        parking_spot = 4
        start_reservation_time = "18:00"
        end_reservation_time = "19:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_not_book_parking_spot_when_his_ending_date_collides_with_another_reservation(
        self,
    ):
        reservation_date = "2020-11-13"
        parking_spot = 1
        start_reservation_time = "19:00"
        end_reservation_time = "21:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_not_book_parking_spot_when_his_starting_date_collides_with_another_reservation(
        self,
    ):
        reservation_date = "2020-11-13"
        parking_spot = 1
        start_reservation_time = "21:00"
        end_reservation_time = "23:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_not_book_parking_spot_when_his_reservation_is_same_as_already_existing_one(
        self,
    ):
        reservation_date = "2020-11-13"
        parking_spot = 1
        start_reservation_time = "20:00"
        end_reservation_time = "22:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_not_book_parking_spot_when_his_reservation_times_are_included_in_already_existing_reservation(
        self,
    ):
        reservation_date = "2020-11-13"
        parking_spot = 1
        start_reservation_time = "21:00"
        end_reservation_time = "21:30"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_book_parking_spot_when_his_reservation_times_are_past_the_existing_one(
        self,
    ):
        reservation_date = "2020-11-13"
        parking_spot = 1
        start_reservation_time = "22:00"
        end_reservation_time = "23:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)

    @freeze_time("2020-11-09 13:00:00")
    def test_max_should_book_parking_spot_when_his_reservation_times_are_before_the_existing_one(
        self,
    ):
        reservation_date = "2020-11-13"
        parking_spot = 1
        start_reservation_time = "19:00"
        end_reservation_time = "20:00"
        username = "Max"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)

    @freeze_time("2020-11-09 13:00:00")
    def test_stephanie_company_B_should_not_book_parking_spot_company_A(
        self,
    ):
        reservation_date = "2020-11-12"
        parking_spot = 10
        start_reservation_time = "19:00"
        end_reservation_time = "20:00"
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2020-11-09 13:00:00")
    def test_stephanie_company_B_should_book_parking_spot_company_B(
        self,
    ):
        reservation_date = "2020-11-12"
        parking_spot = 15
        start_reservation_time = "19:00"
        end_reservation_time = "20:00"
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            start_reservation_time=start_reservation_time,
            end_reservation_time=end_reservation_time,
            username=username,
        )
        self.assertEqual(response_status, status.HTTP_201_CREATED)
