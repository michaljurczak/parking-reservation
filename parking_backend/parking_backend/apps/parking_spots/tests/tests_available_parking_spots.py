# Create your tests here.
from freezegun import freeze_time

from parking_backend.apps.parking_spots.views import (
    AvailableParkingViewSet,
)

from parking_backend.apps.parking_spots.helpers import ParkingTime, ParkingValidators
from parking_backend.apps.parking_spots.constants import DATEFORMAT
from .initial_test_setup import InitialTestSetup


class AvailableParkingSpotsTests(InitialTestSetup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = AvailableParkingViewSet()

    def _run_test_case_and_return_qs_len(
        self, query_date, query_time, parking_spot=None
    ):
        self.view.kwargs = {
            "date": query_date,
            "time": query_time,
        }

        date = ParkingValidators.validate_date_and_time_format(query_date).date()

        if not self.view.get_queryset():
            return None
        if parking_spot:
            return (self.view.get_queryset()
                .get(place_number=parking_spot)
                .reservation_set
                .filter(reservation_date=date)
                .count()
            )
        return self.view.get_queryset()

    @freeze_time("2020-11-09 10:00:00")
    def test_should_be_1_reservations_for_parking_spot_1_for_current_day(self):
        query_date = "2020-11-09"
        query_time = "15:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, 1)

    @freeze_time("2020-11-09 10:00:00")
    def test_should_be_no_parking_spot_1_reservations_in_2_days(self):
        query_date = "2020-11-11"
        query_time = "15:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot = parking_spot,
        )
        self.assertEqual(qs_len, 0)

    @freeze_time("2020-11-09 10:00:00")
    def test_should_not_get_parking_spots_from_the_past(self):
        query_date = "2020-11-08"
        query_time = "15:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, None)

    @freeze_time("2020-11-09 10:00:00")
    def test_should_not_get_parking_spots_week_in_advance(self):
        query_date = "2020-11-16"
        query_time = "10:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, None)

    @freeze_time("2020-11-09 10:00:00")
    def test_should_not_get_parking_spots_month_in_advance(self):
        query_date = "2020-12-09"
        query_time = "10:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, None)

    @freeze_time("2020-11-11 10:00:00")
    def test_should_not_get_parking_spots_for_sunday(self):
        query_date = "2020-12-15"
        query_time = "10:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, None)

    @freeze_time("2020-11-13 15:00:00")
    def test_should_get_1_parking_spot_reservation_for_friday_when_is_friday_3_pm(self):
        query_date = "2020-11-13"
        query_time = "15:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot
        )
        self.assertEqual(qs_len, 1)

    @freeze_time("2020-11-13 14:59:00")
    def test_should_not_get_parking_spots_for_next_friday_when_is_friday_2_59_pm(self):
        query_date = "2020-11-20"
        query_time = "09:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, None)

    @freeze_time("2020-11-13 15:00:00")
    def test_should_get_no_parking_spots_reservations_for_next_friday_when_is_friday_3_pm(self):
        query_date = "2020-11-20"
        query_time = "09:00:00"
        parking_spot = 3

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot
        )
        self.assertEqual(qs_len, 0)

    @freeze_time("2020-11-13 15:01:00")
    def test_should_get_7_parking_spots_for_next_friday_when_is_friday_3_01_pm(self):
        query_date = "2020-11-20"
        query_time = "09:00:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        qs_len = self.view.get_queryset().count()

        self.assertEqual(qs_len, 7)

    @freeze_time("2020-11-13 15:01:00")
    def test_should_get_1_parking_spot_reservation_for_current_friday_when_is_friday_3_01_pm(self):
        query_date = "2020-11-13"
        query_time = "15:10:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, 1)

    @freeze_time("2020-11-13 15:01:00")
    def test_should_not_get_parking_spots_for_next_saturday_when_is_friday_3_01_pm(
        self,
    ):
        query_date = "2020-11-21"
        query_time = "15:10:00"
        parking_spot = 1

        qs_len = self._run_test_case_and_return_qs_len(
            query_date=query_date,
            query_time=query_time,
            parking_spot=parking_spot,
        )
        self.assertEqual(qs_len, None)
