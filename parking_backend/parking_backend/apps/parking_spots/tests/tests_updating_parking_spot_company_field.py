from django.urls import reverse

from rest_framework import status
from rest_framework.test import force_authenticate

from parking_backend.apps.parking_spots.views import (
    UpdateParkingSpotViewSet,
)

from parking_backend.apps.parking_spots.models import (
    ParkingUser,
    Company,
)

from .initial_test_setup import InitialTestSetup


class UpdateCompanyParkingSpotsTests(InitialTestSetup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = UpdateParkingSpotViewSet.as_view()

    def _run_test_case_and_return_http_status(self, parking_spot, company_id, username):
        request_data = {"place_number": parking_spot, "company": company_id}
        request = self.request_factory.put(
            reverse("update_parking_spot"), request_data, "application/json"
        )
        username = username
        try:
            user = ParkingUser.objects.get(username=username)
            force_authenticate(request, user=user)
        except ParkingUser.DoesNotExist:
            pass  # User is not authenticated

        return self.view(request).status_code

    def test_unauthenticated_user_should_not_update_parking_spot_company_name(self):
        parking_spot = 1
        company = 1
        username = ""

        response_status = self._run_test_case_and_return_http_status(
            parking_spot, company, username
        )
        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)

    def test_not_admin_user_stephanie_should_not_update_parking_spot_company_name(self):
        parking_spot = 1
        company = 1
        username = "Stephanie"

        response_status = self._run_test_case_and_return_http_status(
            parking_spot, company, username
        )
        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)

    def test_admin_user_should_update_parking_spot_company_name(self):
        parking_spot = 2
        username = "admin"
        company = Company.objects.get(name="A")
        company = company.id
        response_status = self._run_test_case_and_return_http_status(
            parking_spot, company, username
        )
        self.assertEqual(response_status, status.HTTP_200_OK)

    def test_admin_user_should_not_update_not_existing_parking_spot(self):
        parking_spot = 132323232
        company = 36
        username = "admin"

        response_status = self._run_test_case_and_return_http_status(
            parking_spot, company, username
        )
        self.assertEqual(response_status, status.HTTP_404_NOT_FOUND)

    def test_admin_user_should_not_update_parking_spot_with_not_existing_company(self):
        parking_spot = 1
        company = 3623323232
        username = "admin"

        response_status = self._run_test_case_and_return_http_status(
            parking_spot, company, username
        )
        self.assertEqual(response_status, status.HTTP_400_BAD_REQUEST)
