"""validate unhelpful.robinhood tools"""

import pytest

import requests

from unhelpful import robinhood
from unhelpful import exceptions


@pytest.mark.rh
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


@pytest.mark.rh
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


@pytest.mark.rh
class TestGetInfo:
    """validates get_* queries and their weirdness"""

    def test_get_price(self, rh_client):
        """validate get_price functionality"""
        # No `endpoint`.  Want to validate app.cfg has correct addresses
        price = robinhood.get_price('MU', rh_client)

        assert price
        assert isinstance(price, float)

    def test_get_price_error(self, rh_client):
        """validate bad behavior"""
        with pytest.raises(requests.RequestException):
            price = robinhood.get_price('FAKE', rh_client)

    def test_get_name(self, rh_client):
        """validate get_name functionality"""
        company_name = robinhood.get_name('MU', rh_client)

        assert company_name == 'Micron Technology'

    def test_get_name_failed(self, rh_client):
        """validate bad behavior"""
        with pytest.raises(exceptions.TickerNotFound):
            company_name = robinhood.get_name('FAKE', rh_client)
