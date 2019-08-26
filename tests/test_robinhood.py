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


@pytest.fixture
def rh_client(rh_secrets):
    """fixture to DRY rh tests

    Returns:
        RobinhoodConnection: connection context

    """
    with robinhood.RobinhoodConnection(
        username=rh_secrets.robinhood_username,
        password=rh_secrets.robinhood_password,
        client_id=rh_secrets.robinhood_client_id,
    ) as client:
        yield client


class TestGetInfo:
    """validates get_* queries and their weirdness"""

    def test_get_price(self, rh_client):
        price = robinhood.get_price('MU', rh_client)

        assert price
        assert isinstance(price, float)

    def test_get_name(self, rh_client):
        company_name = robinhood.get_name('MU', rh_client)

        assert company_name == 'Micron Technology'

    def test_get_name_failed(self, rh_client):
        with pytest.raises(exceptions.TickerNotFound):
            company_name = robinhood.get_name('FAKE', rh_client)
