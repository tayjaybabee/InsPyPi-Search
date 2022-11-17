"""

File: inspypi_search/utils/data.py
Project: InsPyPi-Search
Description: 

Created: 11/8/22 - 20:43:12

"""
from re import sub

from pandas import DataFrame

HEADERS = [
        'Package Name',
        'Repository',
        'Installed',
        'Local Version',
        'Latest Version'
]


def parse_to_dict(data):
    res = {}
    for line in data:
        if ' - ' in line:
            pkg, repo = line.split(' - ')
            pkg_spl = pkg.split(' ')
            pkg = pkg_spl[0]
            local_ver = None
            if len(pkg_spl) >= 2:
                local_ver = pkg_spl[1]

            repo = repo.split('/')[-1]
            res[pkg] = {
                    'repo':              repo,
                    'installed_locally': str('False'),
                    'installed':         str(local_ver),
                    'latest':            str(None),
                    'pypi_Url':          f'https://pypi.org/project/{pkg}'

            }

    return res


def remove_consecutive_whitespace(txt):
    """
    The remove_consecutive_whitespace function removes all consecutive whitespace from the input string.

    Here's an example of its usage:

        Rather contrived example below; take a variable 'my_str' and give it a value with consecutive whitespace,
        and then fix that::

            my_str = "This    is a string   with        a bunch of   random whitespace"
            my_str = remove_consecutive_whitespace(my_str)
            print(my_str)
            OUT -> 'This is a string with a bunch of random whitespace'

    Args:
        txt (str):
            Pass the text that needs to be cleaned

    Returns:
        str:
            A string with all the consecutive whitespace characters replaced by a single space

    """
    return sub('\s+', ' ', txt)


def remove_unwanted_characters(txt, unwanted_characters, replace_with: str = ''):
    """
    Doesn't work on commas

    Arguments:
        txt (string):
            The string from which to remove the unwanted characters.

        unwanted_characters (list):
            A list of character strings to be replaced with a specified character (or set thereof). (Required)

        replace_with (Optional, string):
            The character string that should replace the characters specified in the :param:`unwanted_characters`
            parameter value. (Defaults to; '' (no, replacement))


    """
    uc = None

    if not isinstance(txt, str):
        raise TypeError("The 'txt' parameter of the :func:`remove_unwanted_characters` function must be of type "
                        f":class:`str`, not '{type(txt)}'!")

    if not isinstance(unwanted_characters, (str, list, tuple)):
        raise TypeError(f"'unwanted_characters' must be one of str, list, or tuple. Not '{type(unwanted_characters)}'")

    if isinstance(unwanted_characters, (list, tuple)):
        uc = unwanted_characters
    elif isinstance(unwanted_characters, str):

        if ',' in unwanted_characters:
            unwanted_characters = unwanted_characters.replace(' ', '')
            uc = unwanted_characters.split(',')
        elif ' ' not in unwanted_characters and len(unwanted_characters) == 1:
            uc = [unwanted_characters]
        elif ' ' not in unwanted_characters and len(unwanted_characters) > 1:
            uc = list(unwanted_characters)
        else:
            uc = unwanted_characters.split(' ')

    if uc is None:
        raise ValueError('Did not receive proper character set.')

    for char in uc:
        txt = txt.replace(char, replace_with)

    return remove_consecutive_whitespace(txt)


def pack_table(data):
    rows = []
    for item in data.items():
        row = [item[0], *item[1].values()]
        rows.append(row)

    return rows


def get_results_dataframe(results, column_headers):
    return DataFrame(
        data = results,
        columns = column_headers
    )
