import treepy.columns as columns
from typing import (
    Protocol,
    TypeVar,
    Generic,
    Sequence,
    Callable,
    Tuple,
    Optional,
)


NodeType = TypeVar('NodeType', bound='Node')

class Node(Protocol, Generic[NodeType]):
    '''Represents nodes of trees.

    Attributes:
        children (Sequence[NodeType]): Children nodes of the instance.
    '''
    children: Sequence[NodeType]


Left = Sequence[Node]

Right = Sequence[Node]

Stringifier = Callable[[Node], str]

Separator = Callable[[Node], Tuple[Left, Right]]


def v(
        node: Node,
        to_string: Stringifier,
        separate: Separator) -> columns.Column:
    '''Returns the string representing tree structure for a given node.

    Args:
        node (Node): Current node to be processed.
        to_string (Stringifier): Function to be called when the node is stringify.
        separator (Separator): Function to be called when the children of the current node is separated.

    Returns:
        Sequence[str]: Human readable string representation of the node.
    '''
    name = to_string(node)
    l, r = separate(node)
    formatter = lambda n: v(n, to_string, separate)
    lcolumn = columns.left(map(formatter, l)) if l else ()
    rcolumn = columns.right(map(formatter, r)) if r else ()
    children = tuple(
        columns.connect(lcolumn, rcolumn) if l or r else ()
    )
    llen, rlen = columns.get_width(lcolumn), columns.get_width(rcolumn)
    name = f"{' ' * (llen - (len(name) // 2))}{name}{' ' * (rlen - (len(name) // 2))}"
    return columns.combine([[name, *children]])


def h(
        node: Node,
        acc: columns.Column,
        to_string: Stringifier,
        separate: Separator,
        indent: str = '',
        prev: str = 'topbottom') -> None:
    '''Returns the string representing tree structure for a given node.

    Args:
        node (Node): Current node to be processed.
        acc (Columns): Accumulater of the string representation.
        to_string (Stringifier): Function to be called when the node is stringify.
        separator (Separator): Function to be called when the children of the current node is separated.
    '''
    name = to_string(node)
    up, down = separate(node)

    for child in up:
        h(
            child,
            acc,
            to_string,
            separate,
            f'{indent}{" " if "top" in prev else "|"}{" " * len(name)}',
            'top' if up.index(child) == 0 else ''
        )

    if prev == 'top':
        l = '┌'
    elif prev == 'bottom':
        l = '└'
    elif prev == 'topbottom':
        l = ' '
    else:
        l = '├'

    if up:
        r = '┤'
    elif down:
        r = '┐'
    else:
        r = ' '

    acc.append(f'{indent}{l}{name}{r}')

    for child in down:
        h(
            child,
            acc,
            to_string,
            separate,
            f'{indent}{" " if "bottom" in prev else "|"}{" " * len(name)}',
            'bottom' if down.index(child) == len(down) - 1 else ''
        )


def format(node: Node, to_string: Stringifier = lambda n: str(n), horizontal=False) -> str:
    '''Prints out the tree of a given node.

    Args:
        node (Node): Node to be printed

    Returns:
        str: Resulting human readable representation of a specified tree.
    '''
    card = lambda n: sum(card(c) for c in n.children) + 1
    def separate(node: Node) -> Tuple[Sequence[Node], Sequence[Node]]:
        cardinalities = { c: card(c) for c in node.children }
        l = sorted(node.children, key=lambda n: card(n))
        r = []
        while l and sum(cardinalities[n] for n in r) < sum(cardinalities[n] for n in l):
            r.append(l.pop())
        return l, r
    if horizontal:
        columns = []
        h(node, columns, to_string, separate)
        return '\n'.join(columns)
    else:
        return '\n'.join(v(node, to_string, separate))
