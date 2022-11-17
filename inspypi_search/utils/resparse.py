"""

File: inspypi_search/utils/resparse.py
Project: InsPyPi-Search
Description: 

Created: 11/8/22 - 15:28:20

"""
from inspypi_search.utils import to_boolean
from inspypi_search.utils.data import parse_to_dict, remove_unwanted_characters


class ResParse(object):
    offensive_characters = {
            'brackets': [
                    '[',
                    ']'
            ],

            'parens':   [
                    '(',
                    ')'
            ]
    }

    def __init__(
            self,
            results: tuple,
            auto_clean: bool = True,
            auto_parse: bool = True,
            auto_table: bool = True,
            auto_frame: bool = True,
            fill_on_call: bool = True
    ):

        # Create some protected attributes for the parameters to be grabbed by the property getters later.
        self.__cleaned_results = None
        self.__cleaned = False
        self.__auto_clean = auto_clean
        self.__auto_parse = auto_parse
        self.__auto_table = auto_table
        self.__auto_frame = auto_frame
        self.__fill_on_call = fill_on_call
        self.__formatted_results = None

        # Fill some variables with the first stages of our data cleaning.
        self.__tuple = results
        self.__raw = self.__tuple
        self.__raw_utf8 = self.__raw[0]

        # ...and now some attribute defaults for protected properties.

        self.__lines = None
        self.__formatted_lines = None

        if self.auto_clean:
            self.clean()

    @property
    def auto_clean(self):
        return self.__auto_clean

    @property
    def auto_parse(self):
        return self.__auto_parse

    @property
    def auto_table(self):
        return self.__auto_table

    @property
    def auto_frame(self):
        return self.__auto_frame

    @property
    def res_tuple(self):
        return self.__tuple

    @property
    def raw(self):
        return self.res_tuple

    @property
    def raw_utf8(self):
        return self.raw[0]

    @property
    def fill_on_call(self):
        return self.__fill_on_call

    @fill_on_call.setter
    def fill_on_call(self, new):
        try:
            new = to_boolean(new)
        except (ValueError, TypeError) as e:
            print(e)
            raise AttributeError('Attribute "fill_on_call" must be a boolean.') from e
        self.__fill_on_call = new

    @property
    def lines(self):
        """
        Contains the lines of the search results from command output.

        This really just returns ``<output_tuple>[0].splitlines()``
        :return:
        """
        if self.__lines is None and self.__fill_on_call:
            self.__lines = self.raw_utf8.splitlines()

        return self.__lines

    @property
    def result_count(self) -> int:
        """
        The number of results found by the search.
        """
        return len(self.lines)

    def clean(self):
        if not self.__cleaned_results:
            self.__cleaned_results = [self.format_line(line) for line in self.lines]

        return self.__cleaned_results

    @property
    def formatted_lines(self):
        """
        This property contains the formatted search results

        The formatted results is the last formation of the search results before they're loaded into the result
        dictionary.

        Returns:
            str

        """
        if self.__formatted_lines is None and self.fill_on_call:
            self.__formatted_lines = [self.format_line(line) for line in self.lines]
        return self.__formatted_lines

    def format_line(self, line):
        """
        The format_line function removes unwanted characters from the line.
        Args:
            self: Access the class attributes
            line: Pass the line of text that is being processed

        Returns:
            The line with the brackets and parentheses removed

        Doc Author:
            Trelent
        """
        uc = [*self.offensive_characters['brackets'], *self.offensive_characters['parens']]

        return remove_unwanted_characters(line, uc)

    @property
    def formatted_results(self):
        if self.__formatted_results is None and self.fill_on_call:
            self.__formatted_results = self.get_sorted_dictionary()
        return self.__formatted_results

    def get_sorted_dictionary(self):
        if self.__formatted_results is None:
            self.__formatted_results = parse_to_dict(self.formatted_lines)

        return self.__formatted_results




    


    @property
    def cleaned(self):
        return self.__cleaned

    @property
    def cleaned_results(self):
        return self.__cleaned_results

    @property
    def package_list(self):
        return list(self.formatted_results.keys())

    def __getitem__(self, item_name):
        return getattr(self, item_name)



test_results = ('pysimplegui (4.60.0)     - [root/pypi] \n  INSTALLED: 4.60.4\n  LATEST:    4.60.0\npysimplegui27 ()  '
                '       - [root/pypi]\npysimpleguiqt (0.35.0)   - [root/pypi] \n  INSTALLED: 0.35.0\n  LATEST:    '
                '0.35.0\npysimpleguiwx ()         -res [root/pypi]\npysimplegui-chess ()     - ['
                'root/pypi]\npysimpleguiweb ()        - [root/pypi]\n  INSTALLED: 0.39.0\n  LATEST:    '
                '\npysimplegui-howdoi ()    - [root/pypi]\npysimplegui-events ()    - [root/pypi]\npysimpleguiplus () '
                '      - [root/pypi]\npysimplegui-exemaker ()  - [root/pypi]\npysimpleguidesigner ()   - ['
                'root/pypi]\npysimpleguidebugger () - [root/pypi]\n', 0)


# res = {}
#
#
# def remove_brackets(line):
#     return line.replace('[', '').replace(']', '')
#
#
# def remove_parentheses(line):
#     return line.replace('(', '').replace(')', '')
#
#
# def format_line(line):
#     return remove_brackets(remove_parentheses(line))
#
#
# def clean_results(results):
#     return [format_line(line) for line in results.split('\n')]
#
#
# def sort_results(lines):
#     if isinstance(lines, tuple):
#         lines = lines[0]
#     if '\n' in lines:
#         lines = lines.split('\n')
#     for line in lines:
#         if line.startswith('  '):
#             if res == { }:
#                 raise RuntimeError('Package details seemingly arrived before package name')
#             toc = list(res.keys())
#             last = res[toc[-1]]
#             key, value = line.split(':')
#             last[key.lower().replace(' ', '')] = value.replace(' ', '')
#             last['installed_locally'] = True
#         else:
#             print(line)
#             if ' - ' in line:
#                 print(line.split(' - '))
#                 pkg, repo = line.split(' - ')
#                 pkg_spl = pkg.split(' ')
#                 pkg = pkg_spl[0]
#                 print(len(pkg_spl))
#                 print(pkg_spl)
#                 local_ver = None
#                 if len(pkg_spl) >= 2:
#                     local_ver = pkg_spl[1]
#
#                 repo = repo.split('/')[-1]
#                 res[pkg] = {
#                         'repo':              repo,
#                         'installed_locally': False,
#                         'installed':         local_ver,
#                         'latest':            None,
#                         'pypi_Url':          f'https://pypi.org/project/{pkg}'
#
#                 }
#
#     return res


def parse_results(results):
    clean = clean_results(results)
