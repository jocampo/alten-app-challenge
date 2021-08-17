from datetime import datetime


class DateUtils:
    """
    Class holding date utils as needed in the API
    """
    @staticmethod
    def convert_str_to_datetime(date_string: str) -> datetime:
        """
        Converts a string representation of a datetime into a datetime object.
        String format used is that of ISO 8601 (YYYY-MM-DDTHH:MM:SS.ffffff)
        :param date_string: string representation of a datetime
        :return: parsed datetime object
        """
        assert isinstance(date_string, str), type(date_string)
        assert len(date_string) > 0
        return datetime.strptime(date_string, DateUtils.DEFAULT_DATE_STRING_FORMAT)

    @staticmethod
    def convert_datetime_to_iso_str(dt: datetime) -> str:
        """
        Converts a datetime into a string representation of it using the ISO 8601 format
        Output format: YYYY-MM-DDTHH:MM:SS.ffffff (i.e.: 2021-08-20T19:46:21.343959)
        :param dt: datetime to be parsed
        :return: string representation of the provided datetime
        """
        assert isinstance(dt, datetime), type(dt)
        return dt.isoformat()

    """ Default date string format used for the API per ISO 8601 format """
    DEFAULT_DATE_STRING_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
