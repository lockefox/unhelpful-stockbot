"""gather cryptocoin data from resources"""
import collections
import datetime
import enum
import logging
import random

import requests

from . import exceptions
from .utilities import get_config


class CoinSource(enum.Enum):
    coinmarketcap = 'coinmarketcap'


CoinQuote = collections.namedtuple(
    'CoinQuote', ['name', 'symbol', 'price_usd', 'quote_time', 'quote_source']
)


def get_coinmarketcap_list(endpoint=get_config('COINMARKETCAP', 'endpoint')):
    """fetch top coins by marketcap from `coinmarketcap.com`

    Args:
        endpoint (str): endpoint address

    Returns:
        list: list from coinmarketcap

    Raises:
        requests.RequestException: connection/http errors

    """
    req = requests.get(endpoint)
    req.raise_for_status()
    return req.json()


def get_coin_quotes(source=CoinSource.coinmarketcap):
    """get collection of cryptocurrency quotes

    Args:
        source (:enum:`CoinSource`): name/enum of resource to query

    Returns:
        list: collection of CoinQuote named tuples

    Raises:
        requests.RequestException: connection/http errors

    """
    quotes = []
    if CoinSource(source) == CoinSource.coinmarketcap:
        logging.info('fetching quotes from `coinmarketcap`')
        data = get_coinmarketcap_list()
        for record in data:
            quotes.append(
                CoinQuote(
                    name=record['name'],
                    symbol=record['symbol'],
                    price_usd=float(record['price_usd']),
                    quote_time=datetime.datetime.fromtimestamp(int(record['last_updated'])),
                    quote_source=CoinSource.coinmarketcap.value,
                )
            )

        return quotes
