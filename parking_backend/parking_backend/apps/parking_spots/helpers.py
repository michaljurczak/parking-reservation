from datetime import datetime, timedelta
from .constants import (
    DATEFORMAT,
    DATE_AND_TIME_FORMAT,
    WEEKDAY_FRIDAY,
    WEEK_DAYS_NUMBER,
    HOUR_15,
    DATE_AND_TIME_FORMAT,
)


class ParkingTime:
    @staticmethod
    def get_current_time():
        """
        Method for returning current date and time.

        Returns:
        datetime : Returns datetime object with current date.
        """
        return datetime.now()

    @staticmethod
    def is_friday_after_three_pm():
        """
        Method for returning if it is Friday after 3PM

        Returns:
        bool : Returns True if it is Friday after 3PM. In another scenarios, returns False.
        """
        current_date_and_time = ParkingTime.get_current_time()
        if (
            current_date_and_time.weekday() <= WEEKDAY_FRIDAY
            and current_date_and_time.hour < HOUR_15
        ):
            return False
        return True


class ParkingValidators:
    @staticmethod
    def validate_date_and_time_format(query_date_and_time_string):
        """
        Method for date and time format validation.

        Validates if the string value passed to the method is in YYYY-MM-DD HH:MM:SS or YYYY-MM-DD format.

        Parameters:
        query_date_and_time_string (str): Accepts all strings.
        date_and_time_format (str): String format for date and time
        defined in datetime library eg. %Y-%m-%d %H:%M:%S.

        Returns:
        False/datetime: If the date and time format is incorrect,
        the method returns False, in other cases it returns datetime object.
        """
        try:
            return datetime.strptime(query_date_and_time_string, DATE_AND_TIME_FORMAT)
        except ValueError:
            pass
        try:
            return datetime.strptime(query_date_and_time_string, DATEFORMAT)
        except ValueError:
            return False

    @staticmethod
    def validate_parking_requirements(query_date_and_time_string):
        """
        Method for validating the Parking requirements.

        Method, that takes the string as a parameter and validates the Parking requirements.

        Parameters:
        query_date_and_time_string (str): Accepts all strings

        Returns:
        False/datetime.date: In case if the Parking requirements are satisfied,
        it returns datetime.date object in other cases if returns False.
        """
        query_date_and_time = ParkingValidators.validate_date_and_time_format(
            query_date_and_time_string
        )
        if not query_date_and_time:
            return False

        current_date_and_time = ParkingTime.get_current_time()

        if query_date_and_time.weekday() > WEEKDAY_FRIDAY:
            return False

        query_week_number = int(query_date_and_time.strftime("%V"))
        current_date_and_time_week_number = int(current_date_and_time.strftime("%V"))
        week_difference = query_week_number - current_date_and_time_week_number

        if week_difference and not ParkingTime.is_friday_after_three_pm():
            return False

        days_difference = (
            query_date_and_time.date() - current_date_and_time.date()
        ).days

        if (
            days_difference > WEEK_DAYS_NUMBER
        ):  # We want to get available parking spots for the next 7 days
            return False

        return query_date_and_time
