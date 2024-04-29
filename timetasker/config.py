from datetime import timedelta
import os
from pathlib import Path
from timetasker import globals, timeutils
import toml


SECTION_TIMER = "timer"


KEY_WORK_INTERVAL = "work_interval"


DEFAULT_WORK_INTERVAL = "25m"


class Config:
    """
    Exposes supported configuration, data, and cache variables
    """

    def __init__(self) -> None:
        self._config: dict = {}
        self._load_config()

    def _load_config(self) -> None:
        config_filepath = self._config_dir / globals.CONFIG_FILENAME

        if not config_filepath.exists():
            return

        with open(config_filepath, "r") as config_file:
            self._config = toml.load(config_file)

    @property
    def _config_dir(self) -> Path:
        if os.name == "posix":
            config_home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
            return Path(config_home) / globals.APP_NAME
        elif os.name == "nt":
            return Path(os.environ["APPDATA"]) / globals.APP_NAME
        else:
            return Path.home() / "." + globals.APP_NAME

    @property
    def _data_dir(self) -> Path:
        if os.name == "posix":
            # On Linux and macOS, follow XDG Base Directory Specification
            data_home = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
            return Path(data_home) / globals.APP_NAME
        elif os.name == "nt":
            # On Windows, use the user's appdata directory
            return Path(os.environ["APPDATA"]) / globals.APP_NAME / "data"
        else:
            # Fallback for other platforms
            return Path.home() / "." + globals.APP_NAME / "data"

    @property
    def _cache_dir(self) -> Path:
        if os.name == "posix":
            # On Linux and macOS, follow XDG Base Directory Specification
            cache_home = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
            return Path(cache_home) / globals.APP_NAME
        elif os.name == "nt":
            # On Windows, use the user's local appdata directory
            return (
                Path(os.environ.get("LOCALAPPDATA", os.path.join(os.environ["APPDATA"], "Local")))
                / globals.APP_NAME
                / "cache"
            )
        else:
            # Fallback for other platforms
            return Path.home() / "." + globals.APP_NAME / "cache"

    @property
    def data_pickle_filepath(self) -> Path:
        filepath = self._cache_dir / globals.DATA_PICKLE_FILENAME
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        return filepath

    @property
    def _timer_config(self) -> dict:
        return self._config.get(SECTION_TIMER, {})

    @property
    def work_interval_duration(self) -> timedelta:
        return timeutils.parse_duration(self._timer_config.get(KEY_WORK_INTERVAL, DEFAULT_WORK_INTERVAL))


config = Config()
