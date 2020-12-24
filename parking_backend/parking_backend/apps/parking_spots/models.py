from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='company name',
        help_text='Enter company name.',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']


class ParkingSpot(models.Model):
    place_number = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        validators = [MinValueValidator(1)],
        verbose_name='place number',
        help_text='Enter parking spot place number starting from 1.',
    )
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.place_number)

    class Meta:
        ordering = ['place_number']


class ParkingUser(AbstractUser):
    company = models.ForeignKey(to=Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username


class Reservation(models.Model):
    user = models.ForeignKey(to=ParkingUser, on_delete=models.SET_NULL, null=True)
    parking_spot = models.ForeignKey(to=ParkingSpot, on_delete=models.SET_NULL, null=True)
    reservation_date = models.DateField(
        verbose_name='reservation date',
        help_text='Enter parking spot reservation date. Date format: <em>YYYY-MM-DD</em>',
    )
    start_reservation_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='starting parking spot reservation time',
        help_text='Enter starting parking spot reservation time. Time format: <em>HH:MM</em>',
        )
    end_reservation_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='ending parking spot reservation time',
        help_text='Enter ending parking spot reservation time. Time format: <em>HH:MM</em>',
        )

    def __str__(self):
        return f"{self.user} reserved for: {self.reservation_date}"

    class Meta:
        ordering = ['-reservation_date']
