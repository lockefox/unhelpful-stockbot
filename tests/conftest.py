"""pytest utilities/helpers"""
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

    return cfg_path


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
