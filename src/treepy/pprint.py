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


def _vertical(
        node: Node,
        stringify: Stringifier,
        separate: Separator) -> columns.Column:
    '''Returns the string representing tree structure for a given node.

    Args:
        node (Node): Current node to be processed.
        stringify (Stringifier): Function to be called when the node is stringify.
        separator (Separator): Function to be called when the children of the current node is separated.

    Returns:
        Sequence[str]: Human readable string representation of the node.
    '''
    l, r = separate(node)
    formatter = lambda n: _vertical(n, stringify, separate)
    lcolumn = columns.left(map(formatter, l)) if l else ()
    rcolumn = columns.right(map(formatter, r)) if r else ()
    children = tuple(
        columns.connect(lcolumn, rcolumn) if l or r else ()
    )
    name = stringify(node)
    llen, rlen = columns.get_width(lcolumn), columns.get_width(rcolumn)
    name = f"{' ' * (llen - (len(name) // 2))}{name}{' ' * (rlen - (len(name) // 2))}"
    return columns.combine([[name, *children]])


def tree(node: Node, stringify: Callable[[Node], str] = lambda n: str(n)) -> str:
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
    return '\n'.join(_vertical(node, stringify, separate))
