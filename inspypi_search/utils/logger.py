# Our imports
from inspy_logger import InspyLogger

from inspypi_search.__about__ import __PROG__ as PROG, __VERSION__ as VERSION
from inspypi_search.cli.arguments import PARSED_ARGS

LEVEL = PARSED_ARGS.log_level
ROOT_LOGGER = InspyLogger(PROG, LEVEL)

if not ROOT_LOGGER.device.started:
    LOG = ROOT_LOGGER.device.start()
    LOG.info(f'{PROG} - v{VERSION}')


def check_manifest(log_name):
    return log_name.lower() in [key.lower() for key in ROOT_LOGGER.device.manifest.contents.keys()] or None


def get_child(log_name):
    if check_manifest(log_name):
        return ROOT_LOGGER.device.manifest.contents[log_name]['device']
    else:
        return ROOT_LOGGER.device.add_child(log_name)
