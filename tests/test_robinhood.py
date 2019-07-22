"""valudate unhelpful.robinhood tools"""

import pytest
import os


def test_hello_world(rh_secrets):
    """DELETE ME"""
    print(os.environ)
    print(rh_secrets)
    assert True
