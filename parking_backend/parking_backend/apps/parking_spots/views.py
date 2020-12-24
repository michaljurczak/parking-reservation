from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .helpers import ParkingValidators, ParkingTime
from .models import ParkingSpot, Reservation
from .serializers import ParkingSpotSerializer, ReservationSerializer, PeriodReservationSerializer, UpdateParkingSpotSerializer

# Create your views here.
@api_view(['GET'])
def simple_response(request):
    """
    Return simple response
    """
    response_message = {"message": "Parking API working!"}
    return Response(response_message, status=status.HTTP_200_OK)


class AvailableParkingViewSet(generics.ListAPIView):
    """
    Return list of available parking places for certain day and hour

    Parameters:
    date (str): Date in format YYYY-MM-DD
    time (str): Time in format HH:mm
    """
    serializer_class = ParkingSpotSerializer
    lookup_date_kwarg = 'date'
    lookup_time_kwarg = 'time'

    def get_queryset(self):
        """
        Custom queryset for getting available parking spots.

        Returns:
            django.db.models.query.QuerySet: Returns QuerySet object with available parking spots.
        """
        query_date_string = self.kwargs.get(self.lookup_date_kwarg, None)
        query_time_string = self.kwargs.get(self.lookup_time_kwarg, None)
        query_date_and_time_string = f'{query_date_string} {query_time_string}'
        validated_date = ParkingValidators.validate_parking_requirements(query_date_and_time_string)
        now = ParkingTime.get_current_time()
        if not validated_date:
            return None

        if now > validated_date:
            return None
        return ParkingSpot.objects.all().order_by('place_number')


class ReserveParkingSpotViewSet(generics.CreateAPIView):
    """
    Create new parking spot reservation for whole day
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class PeriodReserveParkingSpotViewSet(generics.CreateAPIView):
    """
    Create new parking spot reservation for specific period of time
    """
    serializer_class = PeriodReservationSerializer
    permission_classes = [IsAuthenticated]


class UpdateParkingSpotViewSet(generics.UpdateAPIView):
    """
    Updates parking spot's assigned company
    """
    serializer_class = UpdateParkingSpotSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        place_number = self.request.data['place_number']
        return get_object_or_404(ParkingSpot, place_number=place_number)


class RemoveReservationViewSet(generics.DestroyAPIView):
    """
    Deletes the user reservation for the parking spot
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        reservation.delete()
        return Response(status.HTTP_204_NO_CONTENT)
