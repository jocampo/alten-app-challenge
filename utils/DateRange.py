from datetime import datetime
from typing import NamedTuple


class DateRange(NamedTuple):
    start: datetime
    end: datetime
