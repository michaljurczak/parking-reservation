# System for booking parking spots

## Prerequisites
* Installed [Docker](https://www.docker.com)
--------------------------------------------
## Installation and usage
* Just type the command below in the project root directory to build and run the project:
```ps
docker-compose up
```
* Run frontend and backend docker containers
```ps
docker-compose run backend bash
```
* Create django superuser (for demo purposes use username: admin password: admin, assign company id 2 to the user) inside the backend bash
```ps
./manage.py createsuperuser
```
* Create some parking spots inside backend bash
```ps
./manage.py shell
```
* Inside the shell
```ps
from parking_backend.apps.parking_spots.models import ParkingSpot

for i in range(1, 11):
    ParkingSpot.objects.create(place_number=i)
```
* And enjoy the app!
--------------------------------------------
## Running frontend tests
* Enter parking_frontend bash
```ps
docker-compose run frontend bash
```
* Run
```ps
npm test
```
--------------------------------------------
## Running frontend tests
* Enter parking_backend bash
```ps
docker-compose run backend bash
```
* Run
```ps
./manage.py test
```
--------------------------------------------
## Happy Development!
--------------------------------------------

## Features

    - From Monday the user can only book parking spot for the current week
    - After 3 pm on Friday, the user can book parking spot for the rest of the day on Friday or for the following week
    - Only admin can assign company to the parking spot
    - The user can only once per day (or when the reservation ends) book the parking spot
    - The backend allows to book parking spots for the certain period of time (min. time period - 10 minutes)