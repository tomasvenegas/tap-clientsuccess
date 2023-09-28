"""Stream type classes for tap-clientsuccess."""

import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Union, cast

import pendulum
import requests
from singer.schema import Schema
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.plugin_base import PluginBase as TapBaseClass

from tap_clientsuccess.client import ClientSuccessStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ClientsStream(ClientSuccessStream):
    """Clients stream.

    As of v1, this is a single query with no filter, so no replication key is needed.

    https://clientsuccess.readme.io/reference/listallclients
    """
    name = "clients"
    path = "/clients"
    primary_keys = ["id"]
    replication_key = None  # see doc above
    schema_filepath = SCHEMAS_DIR / "clients.json"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "client_id": record["id"],
        }

class ProductsStream(ClientSuccessStream):
    """Products stream.

    As of v1, this is a single query with no filter, so no replication key is needed.

    https://clientsuccess.readme.io/v1.0/reference/listallproducts
    """
    name = "products"
    path = "/products"
    primary_keys = ["id"]
    replication_key = None  # see doc above
    schema_filepath = SCHEMAS_DIR / "products.json"

class EmployeesStream(ClientSuccessStream):
    """Employees stream.

    As of v1, this is a single query with no filter, so no replication key is needed.

    https://clientsuccess.readme.io/v1.0/reference/listallemployees
    """
    name = "employees"
    path = "/employees"
    primary_keys = ["id"]
    replication_key = None  # see doc above
    schema_filepath = SCHEMAS_DIR / "employees.json"

class StatusesStream(ClientSuccessStream):
    """Statuses stream.

    As of v1, this is a single query with no filter, so no replication key is needed.

    https://clientsuccess.readme.io/v1.0/reference/listallstatuses
    """
    name = "statuses"
    path = "/client-statuses"
    primary_keys = ["id"]
    replication_key = None  # see doc above
    schema_filepath = SCHEMAS_DIR / "statuses.json"


class InteractionsStream(ClientSuccessStream):
    """Interactions Stream

    https://clientsuccess.readme.io/reference/listallinteractionsofaclient
    """
    name = "interactions"
    parent_stream_type = ClientsStream
    ignore_parent_replication_keys = True
    path = "/clients/{client_id}/interactions"
    primary_keys = ["id"]
    replication_key = "createdDateTime"
    schema_filepath = SCHEMAS_DIR / "interactions.json"
    DEFAULT_PAGE_SIZE = 100

    def __init__(
        self,
        tap: TapBaseClass,
        name: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], Schema]] = None,
        path: Optional[str] = None,
    ):
        super().__init__(tap=tap, name=name, schema=schema, path=path)
        self._current_response_new_records_count = 0
        self._page_size = self.DEFAULT_PAGE_SIZE

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if self.new_records_count < self._page_size:
            next_page_token = None
        else:
            next_page_token = 1 if previous_token is None else previous_token + 1
        return next_page_token

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.reset_records_counter()
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        starting_timestamp = self.get_starting_timestamp(context)
        record_replication_key_value = cast(datetime.datetime, pendulum.parse(row[self.replication_key]))
        if starting_timestamp is None or starting_timestamp < record_replication_key_value:
            self.count_record()
            return row
        return None

    def count_record(self):
        self._current_response_new_records_count += 1

    def reset_records_counter(self):
        self._current_response_new_records_count = 0

    @property
    def new_records_count(self):
        return self._current_response_new_records_count


class ClientDetailStream(ClientSuccessStream):
    """Client Detail Stream

    https://clientsuccess.readme.io/reference/getaclientdetail
    """
    name = "client_detail"
    parent_stream_type = ClientsStream
    ignore_parent_replication_keys = True
    path = "/clients/{client_id}"
    primary_keys = ["id"]
    replication_key = "lastModifiedDate"
    schema_filepath = SCHEMAS_DIR / "client.json"

class ClientSuccessStreamV2(ClientSuccessStream):

    url_base = "https://api.clientsuccess.com/v2"
    records_jsonpath = "$.data[*]"

class ClientStreamV2(ClientSuccessStreamV2):
    """Client stream.

    https://clientsuccess.readme.io/reference/searchclients
    """
    name = "clientv2"
    path = "/client/search"
    primary_keys = ["id"]
    replication_key = None  # see doc above
    schema_filepath = SCHEMAS_DIR / "clientv2.json"
    


class ContactStreamV2(ClientSuccessStreamV2):
    """Contact stream.

    https://clientsuccess.readme.io/reference/searchcontacts
    """
    name = "contactsv2"
    path = "/contact/search"
    primary_keys = ["id"]
    replication_key = None  # see doc above
    schema_filepath = SCHEMAS_DIR / "clientv2.json"


class PulseStream(ClientSuccessStream):
    """Client Pulse

    https://clientsuccess.readme.io/v1.0/reference/listallpulsesofaclient
    """
    name = "pulses"
    parent_stream_type = ClientsStream
    ignore_parent_replication_keys = True
    path = "/clients/{client_id}/pulses"
    primary_keys = ["id"]
    replication_key = "createdTimestamp"
    schema_filepath = SCHEMAS_DIR / "pulses.json"

    def __init__(
        self,
        tap: TapBaseClass,
        name: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], Schema]] = None,
        path: Optional[str] = None,
    ):
        super().__init__(tap=tap, name=name, schema=schema, path=path)
        self._current_response_new_records_count = 0

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.reset_records_counter()
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        starting_timestamp = self.get_starting_timestamp(context)
        record_replication_key_value = cast(datetime.datetime, pendulum.parse(row[self.replication_key]))
        if starting_timestamp is None or starting_timestamp < record_replication_key_value:
            self.count_record()
            return row
        return None

    def count_record(self):
        self._current_response_new_records_count += 1

    def reset_records_counter(self):
        self._current_response_new_records_count = 0

    @property
    def new_records_count(self):
        return self._current_response_new_records_count

class ContactStream(ClientSuccessStream):
    """Client Contacts

    https://clientsuccess.readme.io/v1.0/reference/listallcontactsofaclient
    """
    name = "contacts"
    parent_stream_type = ClientsStream
    ignore_parent_replication_keys = True
    path = "/clients/{client_id}/contacts"
    primary_keys = ["id"]
    replication_key = "id"
    schema_filepath = SCHEMAS_DIR / "contacts.json"

    def __init__(
        self,
        tap: TapBaseClass,
        name: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], Schema]] = None,
        path: Optional[str] = None,
    ):
        super().__init__(tap=tap, name=name, schema=schema, path=path)
    
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        return row