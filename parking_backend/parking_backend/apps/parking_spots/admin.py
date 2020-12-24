from django.contrib import admin

from .models import Company, ParkingSpot, Reservation, ParkingUser
# Register your models here.

admin.site.register([
    Company,
    ParkingSpot,
    Reservation,
    ParkingUser,
])
