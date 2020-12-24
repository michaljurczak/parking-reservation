from django.apps import AppConfig


class ParkingSpotsConfig(AppConfig):
    name = 'parking_backend.apps.parking_spots'


default_app_config = 'parking_backend.apps.parking_spots.ParkingSpotsConfig'
