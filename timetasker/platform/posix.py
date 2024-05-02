from .base import PlatformDirsABC
from pathlib import Path
import os


class PosixPlatformDirs(PlatformDirsABC):
    def __init__(self, appname: str) -> None:
        self._appname: str = appname

    @property
    def platform_name(self) -> str:
        return "posix"

    @property
    def config_dir(self) -> Path:
        config_home = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        return Path(config_home) / self._appname

    @property
    def data_dir(self) -> Path:
        data_home = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        return Path(data_home) / self._appname

    @property
    def cache_dir(self) -> Path:
        cache_home = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
        return Path(cache_home) / self._appname
