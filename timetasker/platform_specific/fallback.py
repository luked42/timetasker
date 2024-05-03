from .base import PlatformDirsABC
from pathlib import Path
import os


class FallbackPlatformDirs(PlatformDirsABC):
    def __init__(self, appname: str) -> None:
        self._appname: str = appname

    @property
    def platform_name(self) -> str:
        return "unknown"

    @property
    def config_dir(self) -> Path:
        return Path.home() / f".{self._appname}"

    @property
    def data_dir(self) -> Path:
        return Path.home() / f".{self._appname}" / "data"

    @property
    def cache_dir(self) -> Path:
        return Path.home() / f".{self._appname}" / "cache"
