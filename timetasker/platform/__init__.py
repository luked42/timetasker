import os

if os.name == "posix":
    from .posix import PosixPlatformDirs as PlatformDirs
elif os.name == "nt":
    from .windows import WindowsPlatformDirs as PlatformDirs
else:
    from .fallback import FallbackPlatformDirs as PlatformDirs
