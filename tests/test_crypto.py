"""test crypto quoting tools"""
import logging

import jsonschema
import pytest

from unhelpful import crypto


@pytest.mark.crypto
def test_get_coinmarketcap_list():
    """validate output of coinmarketcap"""
    quote = crypto.get_coinmarketcap_list()
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "rank": {"type": "string"},
                "symbol": {"type": "string", "pattern": "[A-Z]+"},
                "price_usd": {"type ": "string", "pattern": r"\d+\.\d+"},
                "last_updated": {"type": "string", "pattern": r"\d{10}"},
            },
            "required": ["name", "rank", "symbol", "price_usd", "last_updated"],
        },
    }

    jsonschema.validate(quote, schema)


@pytest.mark.crypto
class TestGetCoinQuotes:
    """validate quote fetching tools"""

    def test_coin_quotes_default(self, caplog):
        with caplog.at_level(logging.INFO, logger=''):
            quotes = crypto.get_coin_quotes()
            assert "fetching quotes from `coinmarketcap`" in [r.msg for r in caplog.records]

        assert all([isinstance(quote, crypto.CoinQuote) for quote in quotes])

        bitcoin_quote = [quote for quote in quotes if quote.symbol == 'BTC'][0]
        assert bitcoin_quote.name == 'Bitcoin'

    def test_coin_quotes_coinmarketcap(self, caplog):
        with caplog.at_level(logging.INFO, logger=''):
            quotes = crypto.get_coin_quotes(crypto.CoinSource.coinmarketcap)
            assert "fetching quotes from `coinmarketcap`" in [r.msg for r in caplog.records]

        assert all([isinstance(quote, crypto.CoinQuote) for quote in quotes])

        bitcoin_quote = [quote for quote in quotes if quote.symbol == 'BTC'][0]
        assert bitcoin_quote.name == 'Bitcoin'
