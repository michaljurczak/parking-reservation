from django.urls import re_path
from rest_framework.documentation import include_docs_urls

from .views import (
    simple_response,
    AvailableParkingViewSet,
    ReserveParkingSpotViewSet,
    PeriodReserveParkingSpotViewSet,
    UpdateParkingSpotViewSet,
    RemoveReservationViewSet,
)

urlpatterns = [
    re_path(r"^$", simple_response),
    re_path(
        r"^docs/",
        include_docs_urls(title="Parking API documentation", public=False),
        name="documentation",
    ),
    re_path(
        r"^(?P<date>\d{4}(-\d{2}){2})/(?P<time>\d{2}(:\d{2}){2})/?$",
        AvailableParkingViewSet.as_view(),
        name="available_parking_spots",
    ),
    re_path(
        r"^reserve/?$",
        ReserveParkingSpotViewSet.as_view(),
        name="reserve_parking_day",
    ),
    re_path(
        r"^v2/reserve/?$",
        PeriodReserveParkingSpotViewSet.as_view(),
        name="reserve_parking_time",
    ),
    re_path(
        r"^update-parking-spot/?$",
        UpdateParkingSpotViewSet.as_view(),
        name="update_parking_spot",
    ),
    re_path(
        r"^remove-reservation/(?P<pk>\d+)/?$",
        RemoveReservationViewSet.as_view(),
        name="remove_reservation",
    ),
]
