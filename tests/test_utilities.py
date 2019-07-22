"""pytests for unhelpful.utilities"""
import configparser

import pytest

import unhelpful.utilities as utilities
import unhelpful.exceptions as exceptions


@pytest.mark.incremental
class TestGetConfig:
    """validate get_config performance"""

    def test_pkgutil(self):
        """validate default beahvior -- MUST RUN FIRST"""
        print(utilities.CONFIG_FILE)
        assert utilities.get_config('ROBINHOOD', 'oauth_endpoint')

    def test_happypath(self, config):
        """validate expected behavior"""
        import unhelpful.utilities as t_utilities

        t_utilities.CONFIG_FILE = config

        assert t_utilities.get_config('TEST', 'key1') == 'val1'

    def test_default(self, config):
        """validate default behavior"""
        import unhelpful.utilities as t_utilities

        t_utilities.CONFIG_FILE = config

        assert t_utilities.get_config('FAKE', 'key1', 'default') == 'default'

    def test_error(self, config):
        """valdiate exception case"""
        import unhelpful.utilities as t_utilities

        t_utilities.CONFIG_FILE = config

        with pytest.raises(configparser.Error):
            t_utilities.get_config('FAKE', 'key1')
