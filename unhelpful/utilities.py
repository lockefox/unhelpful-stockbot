"""general helpers for Unhelpful libraries"""

import configparser
import os
import pkgutil

CONFIG_FILEPATH = os.environ.get('USELESS_CONFIG_FILEPATH', pkgutil.get_data('useless', 'app.cfg'))


def get_config(section, key, default=''):
    """fetch valuse from config file

    Args:
        section (str): configparser section
        key (str): configparser key
        default (str): default value

    Returns:
        str: configparser output

    Raises:
        Configparser.exception: unable to locate value

    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILEPATH)

    try:
        val = config.get(section, key)
    except Exception:
        if default:
            return default
        raise

    return val
