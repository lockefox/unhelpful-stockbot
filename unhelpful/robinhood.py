"""utilities for collecting stock quotes from Robinhood"""
import os
import pkgutil

import requests


class RobinhoodConnection:
    """contextmanater for handling authenticated feeds from Robinhood

    Args:
        Username (str): Robinhood Username
        Password (str): Robinhood Password
        client_id (str): Robinhood client_id for oAuth

    """

    def __init__(self, username, password, client_id=''):
        self._client_id = client_id
        if not self._client_id:
            self._client_id = 'TODO'
