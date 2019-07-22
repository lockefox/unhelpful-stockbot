"""general helpers for Unhelpful libraries"""

import configparser
import os
import pkgutil

CONFIG_FILE = pkgutil.get_data('unhelpful', 'app.cfg').decode('utf-8')


def get_config(section, key, default=None):
    """fetch valuse from config file

    Args:
        section (str): configparser section
        key (str): configparser key
        default (str): default value

    Returns:
        str: configparser output

    Raises:
        configparser.Error: unable to locate value

    """
    config = configparser.ConfigParser()
    config.read_string(CONFIG_FILE)

    try:
        val = config.get(section, key)
    except configparser.Error:
        if default is not None:
            return default
        raise

    return val
