"""REST client handling, including ClientSuccessStream base class."""
from pathlib import Path

import requests
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ClientSuccessStream(RESTStream):
    """ClientSuccess stream class."""

    url_base = "https://api.clientsuccess.com/v1"
    records_jsonpath = "$[*]"  # Or override `parse_response`.

    def _login(self):
        """
        {
            "access_token": "04a7xxxx-a562-4ad2-xxx-xxx0bxxxx84",
            "token_type": "Bearer",
            "expires_in": 43200 # 12 hours
        }
        """
        username = self.config["username"]
        password = self.config["password"]
        body = {"username": username, "password": password}
        response = requests.post(
            url=f"https://api.clientsuccess.com/v1/auth",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=body,
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        if not hasattr(self, "access_token"):
            self._login()

        headers = {"Authorization": self.access_token}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers
