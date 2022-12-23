from dataclasses import make_dataclass, dataclass

from inspypi_search.errors.output import TableColumnsLockedError
from inspypi_search.utils.data.structs.table.helpers import sanitize_header


class Meta:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Meta, cls).__new__(cls)
        return cls.instance


class Table:
    __columns = []
    __locked = False
    __rows = []

    __auto_capitalize_header_strings = True

    @staticmethod
    def sanitize_header(header):
        """
        Return the provided string after converting it to lower-case and then replacing all whitespace with '_'

        Args:
            header:
                The string you want sanitized.

        Returns:
            str
        """
        return sanitize_header(header)

    @staticmethod
    def format_header(header):
        """
        Format the header string by;

          * Remove underscores and replace with whitespace.
          * Call `.title` on the resulting string

        Args:
            header:
                The string you want formatted.

        Returns:
            The formatted header string.

        """
        return header.replace('_', ' ').title()

    def __lock(self):
        """
        The lock method is used to lock the object.

        This will prevent further columns being added to the object. This will
        allow the Table object to construct it's row dataclass

        (This method returns nothing.)

        """
        if not self.__locked:
            return False

        index = 0

        def transform_header(cols):
            _h = []
            for col in cols:
                _h.append((self.sanitize_header(col.title), col.value_type))

            return _h

        self.__row = make_dataclass(
            'Row',
            transform_header(self.columns),
            bases=dict,
            namespace={'add_value': lambda self: self.values.append()}

        )

    def __init__(
            self,
            name=None,
            auto_capitalize_header_strings=__auto_capitalize_header_strings
    ):

        self.__name = name

        self.__header = None
        self.__auto_capitalize_header_strings = auto_capitalize_header_strings
        self.__row = None
        self.__formatted_column_title_list = None
        self.__sanitized_column_title_list = None
        self.__column_title_list = None
        self.__foo = None

    @property
    def foo(self):
        if self.__foo is None:
            self.__foo = 'bar'

        return self.__foo

    @foo.deleter
    def foo(self):
        self.__foo = None

    def add_column(self, *args, **kwargs):
        if not self.columns_locked:
            self.__columns.append(self.Column(*args, **kwargs))
            self.header_update(*args, **kwargs)
        else:
            raise TableColumnsLockedError()

    def add_row(self, *args, **kwargs):
        if not self.locked:
            self.lock()

        self.__rows.append(self.Row(*args, **kwargs))

    def header_update(self, title, *args, value_type: type = str, **kwargs):

        # If the table has -no- rows, let's create our header row
        if len(self.rows) == 0:
            self.rows.append([])

        # Format the header string
        if self.auto_capitalize_header_strings:
            title = title.title()

        self.header.append(title)

    def lock(self):
        try:
            if self.locked:
                raise IOError()
        except IOError as e:
            print(e)
            print('Table is already locked.')
            return False

        self.__locked = True

        self.__lock()

        self.__locked = True

    def reset(self):
        del self.columns
        self.__header = []

    @property
    def auto_capitalize_header_strings(self):
        return self.__auto_capitalize_header_strings

    @auto_capitalize_header_strings.setter
    def auto_capitalize_header_strings(self, new):
        if not isinstance(new, bool):
            raise TypeError("'auto_capitalize_header_strings' must contain a boolean value!")

        self.__auto_capitalize_header_strings = new

    @property
    def columns(self):
        return self.__columns

    @columns.deleter
    def columns(self):
        self.__columns = []
        self.__rows = []

    @property
    def columns_locked(self):
        return self.row_count > 0 or self.locked

    @property
    def column_title_list(self):

        if self.__column_title_list is None:
            res = [col.title for col in self.columns]
        else:
            res = self.__column_title_list
        if self.locked:
            self.__column_title_list = res

        return res

    def __Row(self, *args, **kwargs):
        if self.__locked:
            return self.__row(*args, **kwargs)
        else:
            raise NotImplementedError()

    def Row(self, *args, **kwargs):
        try:
            return self.__Row(*args, **kwargs)
        except NotImplementedError as e:
            print('LOCK THE TABLE FIRST')
            raise e from e

    @property
    def sanitized_column_title_list(self):

        if self.__sanitized_column_title_list is None:
            res = [self.sanitize_header(col) for col in self.column_title_list]
        else:
            res = self.__sanitized_column_title_list
        if self.locked:
            self.__sanitized_column_title_list = res

        return res

    @property
    def formatted_column_title_list(self):

        if self.__formatted_column_title_list is None:
            res = [self.format_header(col) for col in self.column_title_list]
        else:
            res = self.__formatted_column_title_list
        if self.locked:
            self.__formatted_column_title_list = res

        return res

    @property
    def locked(self):
        return self.__locked

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new):
        if not isinstance(new, str):
            raise TypeError(f'"name" value must be of type "str" not "{type(new)}"')

        self.__name = new.capitalize()

    @property
    def rows(self):
        return self.__rows

    @rows.deleter
    def rows(self):
        if len(self.rows) > 1:
            self.__rows = [self.rows[0]]

    @property
    def row_count(self):
        return len(self.rows) - 1

    @property
    def header(self):
        return self.rows[0]

    @dataclass
    class Column:
        __slots__ = ('title', 'value_type', 'strict')
        title: str
        value_type: type
        strict: bool

        @property
        def values(self):
            pass
