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
<<<<<<< HEAD
    """validate quote fetching tools
    TODO: parameterize
    """
=======
    """validate quote fetching tools"""
>>>>>>> eed48881a7037d3fa5c6b55e4c7dbba0620dd2e2

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

@pytest.mark.crypto
class TestRandomQuote:
    fake_quotes = [
        crypto.CoinQuote('fake1', 'FK1', 100, 0, 'test'),
        crypto.CoinQuote('fake2', 'FK2', 110, 0, 'test'),
        crypto.CoinQuote('fake3', 'FK3', 120, 0, 'test'),
        crypto.CoinQuote('fake4', 'FK4', 130, 0, 'test'),
        crypto.CoinQuote('fake5', 'FK5', 150, 0, 'test'),
        crypto.CoinQuote('fake6', 'FK6', 140, 0, 'test'),
    ]

    @pytest.mark.random
    def test_get_random_quote_happypath(self):
        """assumes PYTHONHASHSEED=10"""
        quote = crypto.get_random_quote(self.fake_quotes)
        assert quote.name == 'fake3'
        assert quote.symbol == 'FK3'

    def test_get_random_quote_short(self, caplog):
        """todo"""
        with caplog.at_level(logging.INFO, logger=''):
            quote = crypto.get_random_quote(self.fake_quotes, 7)
            assert '`max_range` exceeds actual quote length, using list length: %s' in [
                r.msg for r in caplog.records
            ]

    def test_get_random_quote_zero(self, caplog):
        """todo"""
        with caplog.at_level(logging.INFO, logger=''):
            quote = crypto.get_random_quote(self.fake_quotes, 0)
            assert '`max_range` missing, using full list length: %s' in [
                r.msg for r in caplog.records
            ]
