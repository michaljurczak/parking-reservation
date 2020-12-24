from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory

from .factories import (
    CompanyFactory,
    UserFactory,
    UserGroupFactory,
    ParkingSpotFactory,
    ReservationFactory,
)

from parking_backend.apps.parking_spots.models import (
    ParkingSpot,
    ParkingUser,
    Reservation,
    Company,
)

from .mock_data import MOCK_NAMES, MOCK_RESERVATIONS


class InitialTestSetup(TestCase):
    def _create_parking_users_and_group(self):
        UserGroupFactory.create()

        CompanyFactory(name="A")
        CompanyFactory(name="B")

        company_a = Company.objects.get(name="A")
        company_b = Company.objects.get(name="B")

        UserFactory(username='admin', is_staff=True, company=company_a)

        for name in MOCK_NAMES:
            UserFactory(username=name, company=company_b)

    def _create_parking_spots(self):
        for place_number in range(1, 6):
            ParkingSpotFactory.create(place_number=place_number)

        company_a = Company.objects.get(name="A")
        company_b = Company.objects.get(name="B")
        ParkingSpotFactory.create(place_number=10, company=company_a)
        ParkingSpotFactory.create(place_number=15, company=company_b)

    def _make_mock_reservations(self):
        for mock_reservation in MOCK_RESERVATIONS:
            user = ParkingUser.objects.get(username=mock_reservation["username"])
            for reservation in mock_reservation["reservations"]:
                parking_spot = ParkingSpot.objects.get(
                    place_number=reservation["parking_spot_id"]
                )
                ReservationFactory.create(
                    user=user,
                    parking_spot=parking_spot,
                    reservation_date=datetime.strptime(
                        reservation["parking_spot_reservation_date"],
                        "%Y-%m-%d",
                    ),
                    start_reservation_time=reservation['start_reservation_time'],
                    end_reservation_time=reservation['end_reservation_time'],
                )

    def setUp(self):
        self.request_factory = RequestFactory()
        self._create_parking_users_and_group()
        self._create_parking_spots()
        self._make_mock_reservations()
