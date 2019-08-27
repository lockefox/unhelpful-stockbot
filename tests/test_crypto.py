"""test crypto quoting tools"""
import jsonschema
import pytest

from unhelpful import crypto


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
