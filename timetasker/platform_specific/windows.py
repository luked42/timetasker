from .base import PlatformDirsABC
from pathlib import Path
import os


class WindowsPlatformDirs(PlatformDirsABC):
    def __init__(self, appname: str) -> None:
        self._appname: str = appname

    @property
    def platform_name(self) -> str:
        return "posix"

    @property
    def config_dir(self) -> Path:
        return Path(os.environ["APPDATA"]) / self._appname

    @property
    def data_dir(self) -> Path:
        return Path(os.environ["APPDATA"]) / self._appname / "data"

    @property
    def cache_dir(self) -> Path:
        return (
            Path(os.environ.get("LOCALAPPDATA", os.path.join(os.environ["APPDATA"], "Local"))) / self._appname / "cache"
        )
