__version_info__ = (1, 0, 0)

__version__ = '.'.join(map(str, __version_info__))

VERSION = __version__

from treepy.pprint import pprint

__all__ = [
    'pprint'
]
