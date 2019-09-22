"""gather cryptocoin data from resources"""
import collections
import datetime
import enum
import logging
import random
import os

import requests

from . import exceptions
from .utilities import get_config

c_random = random.Random(os.environ.get('PYTHONHASHSEED'))


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


def get_random_quote(quote_list, max_range=int(get_config('COINMARKETCAP', 'top_coins'))):
    """pick a random cryptocoin to use in actual result

    Args:
        quote_list (list): List of CoinQuote
        max_range (int): maximum for random.randint()

    Returns:
        CoinQuote: single CoinQuote picked randomly

    """
    if max_range > len(quote_list):
        logging.warning(
            '`max_range` exceeds actual quote length, using list length: %s', len(quote_list)
        )
        max_range = len(quote_list)

    if not max_range:
        logging.warning('`max_range` missing, using full list length: %s', len(quote_list))
        max_range = len(quote_list)

    return quote_list[c_random.randint(0, max_range)]
