from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from flask.json import JSONEncoder

from api.entities.ReservationStatus import ReservationStatus


class CustomJSONEncoder(JSONEncoder):
    """
    Override default JSON Encoder to add explicit parsing support for certain objects (like datetimes)
    This allows us to set a known format and not depend on a potentially changing configuration
    """
    def default(self, o: Any) -> Any:
        if type(o) == timedelta:
            return str(o)
        elif type(o) == datetime:
            # TODO: Keep TZ info, which we don't need right now
            return o.replace(tzinfo=None).isoformat()
        elif issubclass(o.__class__, Enum):
            return o.value
        else:
            return super().default(o)
