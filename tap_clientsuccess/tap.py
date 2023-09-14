"""ClientSuccess tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_clientsuccess.streams import (
    ClientsStream,
    InteractionsStream,
    ClientDetailStream,
    ProductsStream,
    PulseStream,
    ContactStream,
    EmployeesStream,
    StatusesStream,
)

STREAM_TYPES = [
    ClientsStream,
    InteractionsStream,
    ClientDetailStream,
    ProductsStream,
    PulseStream,
    ContactStream,
    EmployeesStream,
    StatusesStream,
]


class TapClientSuccess(Tap):
    """ClientSuccess tap class."""
    name = "tap-clientsuccess"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            required=True,
            description="The username to authenticate against the API service"
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            description="The password to authenticate against the API service"
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.clientsuccess.com/v1",
            description="The url for the API service"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
