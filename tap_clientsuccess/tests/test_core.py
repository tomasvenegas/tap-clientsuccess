"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from dotenv import load_dotenv
from singer_sdk.testing import get_standard_tap_tests

from tap_clientsuccess.tap import TapClientSuccess

load_dotenv()

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "username": os.environ.get("TAP_CLIENTSUCCESS_USERNAME", "api_user@example.com"),
    "password": os.environ.get("TAP_CLIENTSUCCESS_PASSWORD", "password")
}


def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        TapClientSuccess,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()
