# treepy

### Install
```
pip install .
```

### Documentation
This package provides:
- a default `Node` protocol
- a `format` function accepting a default `Node` protocol as root

### Example
```python
import sys
import treepy
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
        children = set()
        while edge := user_input.readline(
                is_array=True,
                delimiter=r'\s*,\s*',
                clean=lambda x: x.lstrip('[').rstrip(']')):
            p = memo.setdefault(edge[0], Node(edge[0]))
            c = memo.setdefault(edge[1], Node(edge[1]))
            p.children.append(c)
            children.add(edge[1])
        root = memo[next(iter(set(memo.keys()) - children))]
        print(treepy.format(root, stringify=lambda n: str(n.value)))
        print(treepy.format(root, stringify=lambda n: str(n.value), direction='horizontal'))


if __name__ == '__main__':
    try:
        main()
    except:
        print(format_exc(), file=sys.stderr)
```

Output:
```
                                 1000
 ┌────┬───────────┬───────────────┴──────┐
1140 1150        3000                   2000
           ┌────┬──┴─┬────┬────┐     ┌───┴───────────────────┐
          6000 1300 1130 1120 1400  5000                    4000
                                            ┌────┬────┬────┬──┴───────────────┐
                                           8000 9000 1100 1200               7000
                                                                 ┌────┬────┬──┴─┬────┬────┐
                                                                1500 1600 1700 1110 1900 1800
     ┌1140
     ├1150
     |    ┌6000
     |    ├1300
     ├3000┤
     |    ├1130
     |    ├1120
     |    └1400
 1000┤
     |    ┌5000
     └2000┤
          |    ┌8000
          |    ├9000
          |    ├1100
          |    ├1200
          └4000┤
               |    ┌1500
               |    ├1600
               |    ├1700
               └7000┤
                    ├1110
                    ├1900
                    └1800
```
