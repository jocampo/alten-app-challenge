from datetime import datetime

from utils.DateUtils import DateUtils


class TestDateUtils:
    def test_date_range_no_overlap(self):
        dt1 = datetime.fromisoformat("2021-08-10T00:00:00.343959+00:00")
        dt2 = datetime.fromisoformat("2021-08-20T00:00:00.343959+00:00")

        dt3 = datetime.fromisoformat("2021-08-21T00:00:00.343959+00:00")
        dt4 = datetime.fromisoformat("2021-08-30T00:00:00.343959+00:00")

        assert DateUtils.check_if_date_ranges_overlap(
            dt1, dt2, dt3, dt4
        ) is False

    def test_date_range_overlap(self):
        dt1 = datetime.fromisoformat("2021-08-10T00:00:00.343959+00:00")
        dt2 = datetime.fromisoformat("2021-08-22T00:00:00.343959+00:00")

        dt3 = datetime.fromisoformat("2021-08-21T00:00:00.343959+00:00")
        dt4 = datetime.fromisoformat("2021-08-30T00:00:00.343959+00:00")

        assert DateUtils.check_if_date_ranges_overlap(
            dt1, dt2, dt3, dt4
        ) is True

    def test_date_range_overlap_same_dates(self):
        dt1 = datetime.fromisoformat("2021-08-10T00:00:00.343959+00:00")
        dt2 = datetime.fromisoformat("2021-08-22T00:00:00.343959+00:00")

        dt3 = datetime.fromisoformat("2021-08-10T00:00:00.343959+00:00")
        dt4 = datetime.fromisoformat("2021-08-22T00:00:00.343959+00:00")

        assert DateUtils.check_if_date_ranges_overlap(
            dt1, dt2, dt3, dt4
        ) is True
