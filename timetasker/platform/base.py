from pathlib import Path
from abc import ABC, abstractmethod


class PlatformDirsABC(ABC):
    @property
    @abstractmethod
    def platform_name(self) -> str:
        pass

    @property
    @abstractmethod
    def config_dir(self) -> Path:
        pass

    @property
    @abstractmethod
    def data_dir(self) -> Path:
        pass

    @property
    @abstractmethod
    def cache_dir(self) -> Path:
        pass
