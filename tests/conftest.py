"""pytest utilities/helpers"""
import collections
import configparser
import os
import shutil

import pytest

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(os.path.dirname(HERE), 'unhelpful')


@pytest.fixture
def config(tmpdir, here):
    """generate a dummy config for testing with

    Returns:
        str: path to dummy config

    """
    cfg_path = os.path.join(tmpdir, 'app.cfg')
    shutil.copy(os.path.join(here, 'dummy.cfg'), cfg_path)

    with open(cfg_path, 'r') as cfg_fh:
        return cfg_fh.read()


@pytest.fixture
def rh_secrets():
    """manage secrets, if secrets are not included, xfail the test

    Returns:
        collections.namedtuple: secrets.secret_name=value

    """
    Secret = collections.namedtuple(
        'secret', ['robinhood_username', 'robinhood_password', 'robinhood_client_id']
    )
    test_secrets = Secret(
        robinhood_username=os.environ.get('ROBINHOOD_USERNAME', ''),
        robinhood_password=os.environ.get('ROBINHOOD_PASSWORD', ''),
        robinhood_client_id=os.environ.get('ROBINHOOD_CLIENT_ID', ''),
    )

    if not all([val for val in test_secrets]):
        pytest.xfail('missing required secret')

    return test_secrets


@pytest.fixture
def here():
    """return testdir path

    Returns:
        str: path to test dir

    """
    return HERE


@pytest.fixture
def root():
    """return project path

    Returns:
        str: path to project code

    """
    return ROOT


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)
