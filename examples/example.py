import sys
import treepy.pprint
from dataclasses import dataclass, field
from io import StringIO
from re import split
from textwrap import dedent
from traceback import format_exc
from typing import (
    Any,
    Sequence,
    TypeVar,
    Protocol,
)


NodeType = TypeVar('NodeType', bound='Node')

@dataclass(frozen=True, eq=True)
class Node:
    value: Any
    children: Sequence[NodeType] = field(default_factory=list, compare=False)


class UserInput:
    def __init__(self, text=None):
        self._io = StringIO(text) if text else sys.stdin

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if hasattr(self._io, 'close'):
            self._io.close()

    def readline(self, parse=str, is_array=False, clean=lambda x: x, delimiter=r'\s+'):
        if line := self._readline(clean):
            return [parse(x) for x in split(delimiter, line)] if is_array else parse(line)
        else:
            return None

    def _readline(self, clean):
        if line := self._io.readline():
            return clean(line.strip())
        else:
            return None


INPUT = dedent('''\
[2000,4000]
[1000,2000]
[3000,6000]
[1000,3000]
[2000,5000]
[4000,7000]
[4000,8000]
[4000,9000]
[4000,1100]
[4000,1200]
[3000,1300]
[3000,1400]
[7000,1500]
[7000,1600]
[7000,1700]
[7000,1800]
[7000,1900]
[7000,1110]
[3000,1120]
[3000,1130]
[1000,1140]
[1000,1150]
''')


def main():
    with UserInput(INPUT) as user_input:
        memo = dict()
        not_root = set()
        while edge := user_input.readline(
                is_array=True,
                delimiter=r'\s*,\s*',
                clean=lambda x: x.lstrip('[').rstrip(']')):
            p = memo.setdefault(edge[0], Node(edge[0]))
            c = memo.setdefault(edge[1], Node(edge[1]))
            p.children.append(c)
            not_root.add(edge[1])
        root = next(iter(set(memo.keys()) - not_root))
        root = memo[root]
        tree = treepy.pprint(root, stringify=lambda n: str(n.value))
        print(tree)
        tree = treepy.pprint(root, stringify=lambda n: str(n.value), direction='horizontal')
        print(tree)


if __name__ == '__main__':
    try:
        main()
    except:
        print(format_exc(), file=sys.stderr)
