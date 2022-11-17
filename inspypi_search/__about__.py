"""

File: inspypi_search/__about__.py
Project: InsPyPi-Search
Description:
    Holds program information like its name, version, and author information.

Created: 11/13/22 - 13:29:08

"""
from pathlib import Path

from appdirs import user_cache_dir, user_config_dir, user_state_dir

__PROG__       = 'InsPyPi Search'

__AUTHOR__     = 'Inspyre Softworks'

__VERSION__    = '1.0-dev.1'

__CACHE_DIR__  = Path(user_cache_dir(__PROG__, __AUTHOR__))

__CONFIG_DIR__ = Path(user_config_dir(__PROG__, __AUTHOR__))

__STATE_DIR__  = Path(user_state_dir(__PROG__, __AUTHOR__))
