"""

File: inspypi_search/cli/arguments/standalone_search.py
Project: InsPyPi-Search
Description: 

Created: 11/13/22 - 11:10:53

"""
from argparse import ArgumentParser

from inspy_logger import LEVELS as LOG_LEVELS


class Arguments(ArgumentParser):
    def __init__(self):
        super(Arguments, self).__init__()

        self.prog = 'InsPyPi-Search'
        self.description = 'Search PyPi for packages.'

        self.add_argument(
            'query',
            help='The query to search repositories for.',
            action='store',
            type=str,
            )

        self.add_argument(
            '-M',
            '--max-results',
            help='The maximum number of results to return to the command-line.',
            action='store',
            type=int,
        )

        self.add_argument(
            '-l',
            '--log-level',
            help='The level at which the log outputs messages.',
            choices=LOG_LEVELS,
            action='store',
        )

        self.add_argument(
            '--show-repo',
            help='For each result, show the repository it was found in.',
            action='store_true'
        )

        self.add_argument(
            '-e',
            '--exact-match',
            help='Only show results that literally contain the specified search query.',
            action='store_true',
        )

        self.subparsers = self.add_subparsers(dest='subcommands')

        config_cmd = self.subparsers.add_parser('config')

        config_cmd.add_argument(
            '--show-filepath',
            help='Show the config filepath the the program uses.',
            action='store_true',
        )

        config_cmd.add_argument(
            '-R',
            '--reset',
            help='Reset the configuration file to default values.',
            action='store_true'
        )




args = Arguments()
