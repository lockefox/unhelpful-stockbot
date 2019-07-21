"""pytests for unhelpful.utilities"""
import configparser

import pytest

import unhelpful.utilities as utilities
import unhelpful.exceptions as exceptions


class TestGetConfig:
    """validate get_config performance"""

    def test_happypath(self, config):
        """validate expected behavior"""
        utilities.CONFIG_FILEPATH = config

        assert utilities.get_config('TEST', 'key1') == 'val1'

    def test_default(self, config):
        """validate default behavior"""
        utilities.CONFIG_FILEPATH = config

        assert utilities.get_config('FAKE', 'key1', 'default') == 'default'

    def test_error(self, config):
        """valdiate exception case"""
        utilities.CONFIG_FILEPATH = config

        with pytest.raises(configparser.Error):
            utilities.get_config('FAKE', 'key1')
