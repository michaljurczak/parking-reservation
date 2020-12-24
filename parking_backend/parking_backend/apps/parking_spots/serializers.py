from django.db.models import Q
from datetime import datetime, timedelta, date

from rest_framework import serializers

from .constants import (
    INVALID_DATE_FORMAT,
    NO_RESERVATIONS_LEFT,
    ALREADY_TAKEN,
    MIN_PARKING_SPOT_TIME_SLOT,
    DATE_AND_TIME_FORMAT,
    DATEFORMAT,
    INVALID_COMPANY,
)
from .helpers import ParkingValidators, ParkingTime
from .models import ParkingSpot, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "user", "reservation_date", "parking_spot"]

    def validate(self, data):
        """
        Customized validate method for checking if the user can book
        the parking spot for a specific day.
        According to the Parking requirements

        Parameters:
        data (request): HTTP request

        Returns:
        dict/ValidationError: Dictionary with the validated data
        or ValidationError with a message
        """
        valid_date_format = ParkingValidators.validate_parking_requirements(
            str(data["reservation_date"])
        )

        if not valid_date_format:
            raise serializers.ValidationError(INVALID_DATE_FORMAT)

        user = self.context["request"].user
        if Reservation.objects.filter(
            user=user, reservation_date=valid_date_format
        ).exists():
            raise serializers.ValidationError(NO_RESERVATIONS_LEFT)

        parking_spot = data["parking_spot"]

        if parking_spot.company and parking_spot.company != user.company:
            raise serializers.ValidationError(INVALID_COMPANY)

        if Reservation.objects.filter(
            reservation_date=valid_date_format, parking_spot=parking_spot
        ).exists():
            raise serializers.ValidationError(ALREADY_TAKEN)

        return {
            "user": user,
            "parking_spot": parking_spot,
            "reservation_date": valid_date_format.date(),
        }


class ParkingSpotSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField("get_reservations_for_day")

    def get_reservations_for_day(self, parking_spot):
        date_query = self.context["view"].kwargs.get("date", str(datetime.now().date()))
        date = datetime.strptime(date_query, DATEFORMAT).date()
        qs = Reservation.objects.filter(
            parking_spot=parking_spot, reservation_date=date
        )
        serializer = ReservationSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = ParkingSpot
        depth = 1
        fields = ["place_number", "company", "reservations"]


class UpdateParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = ["place_number", "company"]


class PeriodReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "reservation_date",
            "start_reservation_time",
            "end_reservation_time",
            "parking_spot",
        ]

    def validate(self, data):
        """
        Customized validate method for checking if the user
        can book the parking spot for a specific day and time.
        According to the Parking requirements

        Parameters:
        data (request): HTTP request

        Returns:
        dict/ValidationError: Dictionary with the validated data
        or ValidationError with a message
        """
        valid_date_format = ParkingValidators.validate_parking_requirements(
            str(data["reservation_date"])
        ).date()
        if not valid_date_format:
            raise serializers.ValidationError(INVALID_DATE_FORMAT)
        user = self.context["request"].user
        now = ParkingTime.get_current_time()

        query = Q(user=user, reservation_date=valid_date_format)
        if valid_date_format == now.date():
            query.add(("start_reservation_time__gte", now), "AND")

        if Reservation.objects.filter(query).exists():
            raise serializers.ValidationError(NO_RESERVATIONS_LEFT)

        start_reservation_time = data["start_reservation_time"]
        end_reservation_time = data["end_reservation_time"]
        time_difference = datetime.combine(
            date.min, end_reservation_time
        ) - datetime.combine(date.min, start_reservation_time)

        time_slot = timedelta(minutes=MIN_PARKING_SPOT_TIME_SLOT)

        starting_reservation_date_string = f"{valid_date_format} {end_reservation_time}"
        starting_reservation_date = datetime.strptime(
            starting_reservation_date_string, DATE_AND_TIME_FORMAT
        )

        if time_difference < time_slot or starting_reservation_date < now:
            raise serializers.ValidationError(INVALID_DATE_FORMAT)

        parking_spot = data["parking_spot"]

        if parking_spot.company is not None and parking_spot.company != user.company:
            raise serializers.ValidationError(INVALID_COMPANY)

        if Reservation.objects.filter(
            reservation_date=valid_date_format,
            parking_spot=parking_spot,
            start_reservation_time__lt=end_reservation_time,
            end_reservation_time__gt=start_reservation_time,
        ).exists():
            raise serializers.ValidationError(ALREADY_TAKEN)

        return {
            "user": user,
            "parking_spot": parking_spot,
            "reservation_date": valid_date_format,
            "start_reservation_time": start_reservation_time,
            "end_reservation_time": end_reservation_time,
        }
