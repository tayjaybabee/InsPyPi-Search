"""

File: inspypi_search/config/state.py
Project: InsPyPi-Search
Description: 

Created: 11/14/22 - 12:18:17

"""
import pathlib
from os import makedirs
from shutil import move
from time import time

from inspypi_search.__about__ import __CONFIG_DIR__ as CONFIG_DIR, __STATE_DIR__ as STATE_DIR
from inspypi_search.config.errors import AutoCreateSetTimingError
from inspypi_search.utils import as_bool
from inspypi_search.utils.filesystem import validate_dir, validate_filename

STATE_BACKUP_DIR = STATE_DIR.joinpath('backups')
STATE_FILENAME = 'state.ini'
STATE_FILEPATH = STATE_DIR.joinpath(STATE_FILENAME)


def backup_program_state():
    """
    The backup_program_state function moves the current program state file to a backup directory.
    """
    if not STATE_BACKUP_DIR.exists():
        makedirs(STATE_BACKUP_DIR, exist_ok=True)

    backup_filename = f'{str(time())}.state.backup'
    backup_filepath = STATE_BACKUP_DIR.joinpath(backup_filename)
    move(STATE_FILEPATH, backup_filepath)





class ProgState:

    # Let's add some properties right away...
    __config_dir = CONFIG_DIR
    __config_file_name = 'search.ini'
    __state_dir = STATE_DIR
    __file_path = STATE_DIR.joinpath('state.ini')
    __allow_overwrite = False
    __auto_create = True
    __contents = {
            'search_config_filepath': pathlib.Path(),
            'first_run_timestamp':    0.0,
            'last_run_timestamp':     0.0
    }
    __allow_backup = True

    def __init__(
            self,
            config_file_name: str = __config_file_name,
            config_dir: pathlib.Path = __config_dir,
            allow_overwrite: bool = __allow_overwrite,
            auto_create: bool = __auto_create,
            allow_backup: bool = __allow_backup

    ):
        if not isinstance(allow_overwrite, bool):
            raise ValueError(f"Invalid argument: allow_overwrite must be of type 'bool' not {type(allow_overwrite)}")

        self.config_file_name = config_file_name
        self.config_dir = config_dir

        self.auto_create = auto_create
        self.allow_overwrite = allow_overwrite

        self.allow_backup = allow_backup

    @property
    def allow_backup(self):
        return self.__allow_backup

    @allow_backup.setter
    def allow_backup(self, new):
        self.__allow_backup = as_bool(new)

    @property
    def allow_overwrite(self) -> bool:
        return self.__allow_overwrite

    @allow_overwrite.setter
    def allow_overwrite(self, new):
        self.__allow_overwrite = as_bool(new)

    @property
    def auto_create(self) -> bool:
        return self.__auto_create

    @auto_create.setter
    def auto_create(self, new: bool) -> None:
        if not self.filepath_exists:
            self.__auto_create = as_bool(new)
        else:
            raise AutoCreateSetTimingError()

    @property
    def config_file_name(self) -> str:
        """
        The name of the configuration file.

        Returns:
            str:
                The name of the configuration file.

        """
        return self.__config_file_name

    @config_file_name.setter
    def config_file_name(self, new):
        self.__config_file_name = validate_filename(new)

    @property
    def config_dir(self) -> pathlib.Path:
        """
        The directory which contains the configuration file.


        Returns:
            pathlib.Path:
                The directory which contains the configuration file
        """
        return self.__config_dir

    @property
    def contents(self):
        return self.__contents

    @config_dir.setter
    def config_dir(self, new):
        self.__config_dir = validate_dir(new)

    @property
    def config_dir_exists(self) -> bool:
        """
        The config_dir_exists property checks if the config_dir exists and is a directory.
        If it does, then True is returned. If it doesn't exist or isn't a directory, False is returned.

        **Read-only property**

        Returns:
            True if the config_dir exists and is a directory, otherwise it returns false

        """
        return self.config_dir.exists() and self.config_dir.is_dir()

    @property
    def config_filepath(self) -> pathlib.Path:
        """

        The combined path to the config file concatenated from self.config_dir and self.config_file_name

        Returns:
            pathlib.Path:
                The full filepath of the config file.

        """
        return pathlib.Path(self.config_dir, self.config_file_name).expanduser().resolve()

    @property
    def config_file_exists(self) -> bool:
        """
        Does the config file exist?
        """
        return self.config_filepath.exists() and self.config_filepath.is_file()

    @property
    def dir_path(self) -> pathlib.Path:
        """
        The path to the directory on disk where the state/cache file is stored.

        **Read-only property**
        """
        return self.__state_dir

    @property
    def dir_path_exists(self) -> bool:
        """
        Returns True if the directory exists and is a directory, False otherwise.

        **Read-only property**
        """
        return self.dir_path.exists() and self.dir_path.is_dir()

    @property
    def filepath(self) -> pathlib.Path:
        """
        The location on disk of the cache file.

        **Read-only property**
        """
        return self.__file_path

    @property
    def filepath_exists(self) -> bool:
        """
        Returns True if the cache file exists on disk and is a file. False if either is False.

        **Read-only property**
        """
        return self.filepath.exists()

    def create(self):
        if self.filepath_exists:
            if not self.allow_overwrite:
                raise FileExistsError(f"'{self.filepath}' already exists.")
            self.contents['first_run_timestamp'] = time()
            self.contents['search_config_filepath'] = self.config_filepath
            self.contents['last_run_timestamp'] = time()




    def __getitem__(self, attr_name):
        return getattr(self, attr_name)
