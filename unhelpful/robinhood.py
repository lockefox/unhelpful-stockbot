"""utilities for collecting stock quotes from Robinhood"""
import os
import pkgutil
import logging

import requests

from . import exceptions
from .utilities import get_config


class RobinhoodConnection:
    """contextmanater for handling authenticated feeds from Robinhood

    Args:
        username (str): Robinhood Username
        password (str): Robinhood Password
        client_id (str): Robinhood client_id for oAuth

    """

    def __init__(self, username, password, client_id=''):
        self._client_id = client_id
        if not self._client_id:
            self._client_id = 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS'

        self._username = username
        self._password = password

        self.auth_token = ''
        self.refresh_token = ''

    def get(self, endpoint, params=dict(), headers=dict()):
        """fetch data from endpoint

        Args:
            endpoint (str): what endpoint to fetch data from
            params (dict): params for requests
            headers (dict): headers for requests

        Returns:
            dict: requests.json() output

        Raises:
            requests.RequestException: connection/http errors
            RobinhoodNoLogin: lacking login credentials

        """
        if not any([self.auth_token, self.refresh_token]):
            raise exceptions.RobinhoodNoLogin

        headers = {**headers, 'Authorization': f'Bearer {self.auth_token}'}
        req = requests.get(
            f'{get_config("ROBINHOOD", "root")}/{endpoint}', params=params, headers=headers
        )
        req.raise_for_status()
        return req.json()

    def __enter__(self):
        req = requests.post(
            f'{get_config("ROBINHOOD", "root")}/{get_config("ROBINHOOD", "oauth_endpoint")}',
            params=dict(
                grant_type='password',
                client_id=self._client_id,
                username=self._username,
                password=self._password,
            ),
        )

        req.raise_for_status()
        self.auth_token = req.json()['access_token']
        self.refresh_token = req.json()['refresh_token']
        return self

    def __exit__(self, *exc):
        req = requests.post(
            f'{get_config("ROBINHOOD", "root")}/{get_config("ROBINHOOD", "logout_endpoint")}',
            data=dict(client_id=self._client_id, token=self.refresh_token),
        )
        req.raise_for_status()


def get_price(ticker, client, endpoint=get_config("ROBINHOOD", "quotes_endpoint")):
    """generate a stock quote from Robinhood

    Args:
        ticker (str): stock ticker
        client (:obj:`RobinhoodConnection`): connection context
        endpoint (str): path to

    Returns:
        float: todo

    Raises:
        requests.RequestException: Unable to connect to robinhood

    """
    quote = client.get(endpoint, params={'symbols': ticker})
    if quote['results'][0]['last_extended_hours_trade_price']:
        return float(quote['results'][0]['last_extended_hours_trade_price'])
    return float(quote['results'][0]['last_trade_price'])


def get_name(ticker, client, endpoint=get_config("ROBINHOOD", "instruments_endpoint")):
    """Fetch `simple name` of company given ticker

    Args:
        ticker (str): stock ticker
        client (:obj:`RobinhoodConnection`): connection context
        endpoint (str): endpoint for `instruments` and company trading metadata

    Notes:
        Only smart enough to search 1 page

    Returns:
        str: simple name of company given ticker

    Raises:
        requests.RequestException: unable to conncet to robinhood
        TickerNotFound:
        KeyError: unable to find requested stock ticker

    """
    ticker = ticker.upper()
    instruments = client.get(endpoint, params={'query': ticker})

    company_info = {}
    pageno = 1
    while not company_info:
        for record in instruments['results']:
            if record['symbol'] == ticker:
                company_info = record
                break

        if company_info:  # TODO: this sucks
            break

        if not instruments['next']:
            raise exceptions.TickerNotFound
        instruments = client.get(instruments['next'], params={'query': ticker})

    return company_info['simple_name']
