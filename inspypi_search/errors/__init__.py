"""

File: inspypi_search/errors/__init__.py
Project: InsPyPi-Search
Description: 

Created: 11/14/22 - 12:08:20

"""
import inspect


class InsPyPiSearchError(Exception):
    # Let's set a general error message for the parent exception
    # letting the end-user know that the child exception is
    # of this type;
    p_message = "[InsPyPi Search Error] - An error specific to InsPyPi Search\n"

    def __init__(self, message=None, skip_print=False):
        # If the child exception provides a message we can introduce this with
        # the following phrase;
        msg_prefix = f'\nSome additional context from the raising exception:\n'

        self.__parent_caller_frame = inspect.stack()[1]
        self.__parent_caller_name = self.__parent__caller_frame[3]

        # If we're provided a message on instantiation we'll prepend our prefix
        # to it while assigning it to the :var:`message` variable. If no message
        # was provided :var:`message' will evaluate to str('')
        message = f'{msg_prefix} - {message}' if message is not None else ''

        # Assign our prefix string to a class attribute for easy debugging later.
        self.msg_prefix = msg_prefix

        # finally; contatenate the entirety of the error message delivered on raise.
        self.message = f"{self.p_message}{self.msg_prefix}- {self.message}"

        if not skip_print:
            print(self.message)
