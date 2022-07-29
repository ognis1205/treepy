__version_info__ = (1, 0, 0)

__version__ = '.'.join(map(str, __version_info__))

VERSION = __version__

from treepy.core import Node, format

__all__ = [
    'Node',
    'format'
]
