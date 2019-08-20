"""utilities for collecting stock quotes from Robinhood"""
import os
import pkgutil
import logging

import requests

from . import exceptions

ROOT_URL = 'https://api.robinhood.com'


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

        self.login_endpoint = 'https://api.robinhood.com/oauth2/token/'
        self.logout_endpoint = 'https://api.robinhood.com/oauth2/revoke_token/'
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
        req = requests.get(f'{ROOT_URL}/{endpoint}', params=params, headers=headers)
        req.raise_for_status()
        return req.json()

    def __enter__(self):
        req = requests.post(
            self.login_endpoint,
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
            self.logout_endpoint, data=dict(client_id=self._client_id, token=self.refresh_token)
        )
        req.raise_for_status()
