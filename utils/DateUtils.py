from datetime import datetime

from utils.DateRange import DateRange


class DateUtils:
    """
    Class holding date utils as needed in the API
    """
    @staticmethod
    def convert_str_to_datetime(date_string: str) -> datetime:
        """
        Converts a string representation of a datetime into a datetime object.
        String format used is that of ISO 8601
        :param date_string: string representation of a datetime
        :return: parsed datetime object
        """
        assert isinstance(date_string, str), type(date_string)
        assert len(date_string) > 0
        return datetime.fromisoformat(date_string)

    @staticmethod
    def convert_datetime_to_iso_str(dt: datetime) -> str:
        """
        Converts a datetime into a string representation of it using the ISO 8601 format
        :param dt: datetime to be parsed
        :return: string representation of the provided datetime
        """
        assert isinstance(dt, datetime), type(dt)
        return dt.isoformat()

    @staticmethod
    def check_if_date_ranges_overlap(start_date_a: datetime, end_date_a: datetime, start_date_b: datetime,
                                     end_date_b: datetime) -> bool:
        """
        Utility method to check if 2 date ranges overlap

        :param start_date_a: start of the first date range
        :param end_date_a: end of the first date range
        :param start_date_b: start of the second date range
        :param end_date_b: end of the second date range
        :return: C{True} if the date ranges overlap, C{False} otherwise
        """
        # Sanity checks for the "Date Ranges"
        assert isinstance(start_date_a, datetime), type(start_date_a)
        assert isinstance(end_date_a, datetime), type(end_date_a)
        assert isinstance(start_date_b, datetime), type(start_date_b)
        assert isinstance(end_date_b, datetime), type(end_date_b)

        assert end_date_a > start_date_a
        assert end_date_b > start_date_b

        r1 = DateRange(start=start_date_a, end=end_date_a)
        r2 = DateRange(start=start_date_b, end=end_date_b)

        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)
        delta = int((earliest_end - latest_start).total_seconds()) + 1
        overlap = max(0, delta)
        return overlap > 0
