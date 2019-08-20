"""valudate unhelpful.robinhood tools"""

import pytest
import os

import requests

from unhelpful import robinhood as robinhood


def test_hello_world(rh_secrets):
    """DELETE ME"""
    print(os.environ)
    print(rh_secrets)
    assert False


def test_login(rh_secrets):
    """validate login/logout contextmanager"""
    with robinhood.RobinhoodConnection(
        username=rh_secrets.robinhood_username,
        password=rh_secrets.robinhood_password,
        client_id=rh_secrets.robinhood_client_id,
    ) as client:
        quote = client.get('quotes/', params={'symbols': 'MU'})

    with pytest.raises(requests.RequestException):
        req = requests.get(
            'https://api.robinhood.com/quotes/',
            params={'symbols': 'MU'},
            headers={'Authorization': client.auth_token},
        )
        req.raise_for_status()
