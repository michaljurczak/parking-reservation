from django.contrib.auth.models import Group
import factory

from parking_backend.apps.parking_spots.models import ParkingSpot, Reservation, ParkingUser, Company


class UserGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = 'user'


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParkingUser


class ParkingSpotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParkingSpot


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation
