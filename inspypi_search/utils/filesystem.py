"""

File: inspypi_search/utils/filesystem.py
Project: InsPyPi-Search
Description: 

Created: 11/14/22 - 12:24:24

"""
import pathlib

from pathvalidate import is_valid_filename, sanitize_filename, sanitize_filepath


def validate_dir(
        path: (str | pathlib.Path),
        as_string: bool = False,
        skip_expand: bool = False,
        skip_resolve: bool = False
):
    """
    Validates the given directory path using pathlib.Path after sanitizing it.

    Args:
        path (str|pathlib.Path):
            The directory path to validate.

        as_string (bool, optional):
            The function returns the validated path as a string. After sanitizing, expanding user shortcuts, and
            resolving any symbolic links.

        skip_expand (bool, optional):
            THe function skips the expansion of user directory shortcuts (such as '~').

        skip_resolve:
            The function skips the resolution of links in the path.

    Returns:

    """
    path = sanitize_filepath(path)

    try:
        path = pathlib.Path(path)

        if not skip_expand:
            path = path.expanduser()

        if not skip_resolve:
            path = path.resolve()

        if as_string:
            path = str(path)

    except TypeError as e:
        raise TypeError(f"Invalid directory: {path}") from e

    return path


def validate_filename(filename):
    if not isinstance(filename, str):
        raise TypeError(f"Invalid filename type: {type(filename)}")
    if filename.endswith('.ini'):
        filename = sanitize_filename(filename.strip())
        if is_valid_filename(filename):
            return filename
        else:
            raise ValueError(f"Invalid filename: {filename}")
