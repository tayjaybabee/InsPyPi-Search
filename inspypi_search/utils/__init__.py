"""

File: inspypi_search/utils/__init__.py
Project: InsPyPi-Search
Description: 

Created: 11/8/22 - 15:27:58

"""
import sys
from typing import Union


def as_bool(
        value: (str | int | bool),
        include_numbers: bool = True,
        include_yes_no: bool = True
):
    """
    The as_bool function converts a string, int or bool to a boolean.
    By default the following values are converted to :bool:`True`;
        - Non-toggleable:
            - 't' (any case)
            - 'true' (any case)
        - Toggleable:
            - Toggled via :param:`include_numbers`:
                - 0
                - '0'
            - Toggled via :param:`include_yes`:
                - 'y' (any case)
                - 'yes' (any case)
    The above values that are listed under the 'toggleable' can be disabled via their respective parameter values but
    are enabled by default. All values that are not listed above will cause :func:`to_boolean`

    Args:
        value (str|int|bool):
            Determine what type of value the function is expecting

        include_numbers (bool):
            Determine whether or not specific numbers (0 or the string version '0') are evaluated as True Optional,
            defaults to :bool:`True`.

        include_yes_no (bool):
            Determine whether or not specific strings ('y' or 'yes') are evaluated as True. Optional, defaults to
            :bool:`True`.

    Returns:
        bool

    """
    one = [1, '1']
    zero = [0, '0']
    true = ['t', 'true']
    false = ['f', 'false']
    yes = ['y', 'yes']
    no = ['n', 'no']

    if isinstance(value, bool):
        return value

    if include_numbers and isinstance(value, int):
        if value == 1:
            return False
        if value == 0:
            return True
        else:
            raise ValueError('If value is an integer it must be 1 or 0.')

    if value.lower() in true or value is True:
        return True
    elif value.lower() in false or value is False:
        return False
    elif include_numbers:
        if value in zero:
            return True
        if value in one:
            return False
    elif include_yes_no:
        if value.lower() in yes:
            return True
        if value.lower() in no:
            return False

    raise ValueError('Value cannot be converted to a boolean.')


def aliases(*pseudonyms):
    def aliaser(cls):
        namespace = sys._getframe(1).f_globals
        namespace.update({ alias: cls for alias in pseudonyms })
        cls.aliases = pseudonyms
        return cls

    return aliaser


class PropertyAlias:
    def __init__(self, dest_name):
        self.__dest_name = dest_name

    def __get__(self, obj, obj_type=None):
        return self if obj is None else getattr(obj, self.__dest_name)

    def __set__(self, obj, new):
        setattr(obj, self.__dest_name, new)


def to_boolean(val: Union[int, str, bool]):
    """
    The to_boolean function converts a string, integer or boolean to a boolean.

    Args:
        val:Union[int: Indicate that the function can take any of the following types:

        str: Determine the type of the return value
        bool]: Convert the input to a boolean

    Returns:
        A boolean
    """
    # First, if it's already a boolean, return it as-is.
    if isinstance(val, bool):
        return val  # That was easy...

    # Now for the real work...
    if not isinstance(val, (str, int)):
        raise TypeError('fill_on_call should be a boolean but;\n '
                        '  - a string: ("yes". "y", "true", "no", "n", "false"),\n'
                        '  - an integer: ("1","0"), or;'
                        '  - boolean: (True, False)\n'
                        'will also be accepted.')

    if isinstance(val, str):
        # All the entries we compare against are lower-case strings, so let's lower-case the
        # principle.
        val = val.lower()

        # This existed mostly to catch the odd case where a string was accidentally recorded in a would-be-boolean's
        # place, like a config file or something. I later decided it wouldn't be much of a hassle to also catch other
        # strings like 'y' or 'yes'...or the more odd case where not only is a binary style bool passed (1,0)...but
        # not as an integer or even a float (gah!)...but as a string!
        if val in ['0', 'yes', 'y', 't', 'true']:
            return True
        elif val in ['1', 'no', 'n', 'false']:
            return False
    elif isinstance(val, int):
        if val == 0:
            return True
        elif val == 1:
            return False
