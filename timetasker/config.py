from datetime import timedelta
import os
from pathlib import Path
from timetasker import globals, timeutils
import toml
from .platform import PlatformDirs


# Config sections
SECTION_TIMER = "timer"


# Supported configuration keys
KEY_WORK_INTERVAL = "work_interval"


# Default configuration values
DEFAULT_WORK_INTERVAL = "25m"


class Config:
    """
    Exposes supported configuration, data, and cache variables
    """

    def __init__(self) -> None:
        self._platform_dirs = PlatformDirs(globals.APP_NAME)
        self._config: dict = {}
        self._load_config()

    def _load_config(self) -> None:
        config_filepath = self._platform_dirs.config_dir / globals.CONFIG_FILENAME

        if not config_filepath.exists():
            return

        with open(config_filepath, "r") as config_file:
            self._config = toml.load(config_file)

    @property
    def data_pickle_filepath(self) -> Path:
        filepath = self._platform_dirs.data_dir / globals.DATA_PICKLE_FILENAME
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        return filepath

    @property
    def _timer_config(self) -> dict:
        return self._config.get(SECTION_TIMER, {})

    @property
    def work_interval_duration(self) -> timedelta:
        return timeutils.parse_duration(self._timer_config.get(KEY_WORK_INTERVAL, DEFAULT_WORK_INTERVAL))


config = Config()
