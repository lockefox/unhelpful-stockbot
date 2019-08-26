"""valudate unhelpful.robinhood tools"""

import pytest
import os

import requests

from unhelpful import robinhood
from unhelpful import exceptions


def test_login(rh_secrets):
    """validate login/logout contextmanager"""
    ## Use API as expected ##
    with robinhood.RobinhoodConnection(
        username=rh_secrets.robinhood_username,
        password=rh_secrets.robinhood_password,
        client_id=rh_secrets.robinhood_client_id,
    ) as client:
        quote = client.get('quotes/', params={'symbols': 'MU'})

    ## Validate that client is logged out ##
    with pytest.raises(requests.RequestException):
        req = requests.get(
            'https://api.robinhood.com/quotes/',
            params={'symbols': 'MU'},
            headers={'Authorization': client.auth_token},
        )
        req.raise_for_status()


def test_get_error(rh_secrets):
    """validate handler blows up if not in a `with` context"""
    with pytest.raises(exceptions.RobinhoodNoLogin):
        client = robinhood.RobinhoodConnection(
            username=rh_secrets.robinhood_username,
            password=rh_secrets.robinhood_password,
            client_id=rh_secrets.robinhood_client_id,
        )
        quote = client.get('quotes/', params={'symbols': 'MU'})
