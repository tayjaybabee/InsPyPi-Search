"""

File: inspypi_search/cli/arguments/__init__.py
Project: InsPyPi-Search
Description: 

Created: 11/9/22 - 20:58:50

"""
from argparse import ArgumentParser, Namespace
from typing import Union

from inspy_logger import LEVELS as LOG_LEVELS


class Arguments(object):

    def __init__(self):
        self.__parsed = False
        self.__parsed_args = None
        self.__parser = ArgumentParser()

        self.__parser.add_argument(
            '-l',
            '--log-level',
            action='store',
            choices=LOG_LEVELS,
            help='The level at which you would like the program to output logging data.'

        )

        self.__sub_command_parser = self.__parser.add_subparsers(dest='subcommands')

        self.__search_parser = self.__sub_command_parser.add_parser(
            'search',
            help='Search the repository for the packages matching your query string.',
        )

        self.__search_parser.add_argument(
            'query',
            help='The search query string to search for.',
            action='store'
        )

        self.__search_parser.add_argument(
            '-e',
            '--exact-match',
            action='store_true',
            help='Should the results contain an exact match of the query string?',)

    @property
    def parser(self) -> ArgumentParser:
        """
        This property contains the argparse ArgumentParser instance.

        **Read-only property**

        Returns:
            argparse.ArgumentParser:
        """
        return self.__parser

    @property
    def parsed(self) -> bool:
        """
        Contains a boolean indicating whether the command-line arguments have been parsed yet.

        **Read-only property**

        Returns:
            bool:
                - True:
                    The command-line arguments have been parsed
                -False:
                    The command-line arguments have not yet been parsed.
        """
        return self.__parsed

    @property
    def parsed_args(self) -> Union[Namespace, None]:
        """
        This property returns the parsed command-line arguments if they've been parsed.

         Returns:
             Union[Namespace, None]:
                 The parsed command-line arguments.
        """
        return self.__parsed_args

    def parse(self, *args, **kwargs) -> Namespace:
        """
        A wrapper/alias for ArgumentParser.parse_args().

        The only difference is that this function returns the cached parsed arguments instead of parsing again.

        Returns:
            Namespace:
                The parsed arguments object.
        """
        if not self.parsed:
            self.__parsed_args = self.__parser.parse_args(*args, **kwargs)

        return self.__parsed_args


ARGS = Arguments()
PARSED_ARGS = ARGS.parse()
