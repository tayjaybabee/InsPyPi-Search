"""

File: inspypi_search/config/errors.py
Project: InsPyPi-Search
Description: 

Created: 11/14/22 - 12:08:05

"""
from inspypi_search.errors import InsPyPiSearchError, inspect


class AutoCreateSetTimingError(InsPyPiSearchError):
    # Let's set a more specific message for the child exception.
    message = "[Auto Create Set Timing Error] The timing on setting 'auto_create' for this instance was invalid.\n" \
              " 'auto_create MUST be set prior to state-file creation and will not work if the state-file exists " \
              "on disk."
    prefix = 'Additional context from caller: '

    def __init__(self, message=None, skip_print=False):
        self.__child_caller_frame = inspect.stack()[1]
        self.__child_caller_name = self.__child_caller_frame[3]

        # Prettify our base message string.
        self.message = f"[{self.__class__.__name__}] - {self.message}"

        message = f"{self.prefix} - {message}" if message is not None else ''

        self.message += message

        super(AutoCreateSetTimingError, self).__init__(message = self.message, skip_print = skip_print)
