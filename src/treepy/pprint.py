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
        name (str): Human readable string describing the node.
        parent (Optional[NodeType]): Parent node of the instance if it exists.
        children (Sequence[NodeType]): Children nodes of the instance.
    '''
    name: str
    parent: Optional[NodeType]
    children: Sequence[NodeType]


Left = Sequence[Node]

Right = Sequence[Node]

Stringifier = Callable[[Node], str]

Separator = Callable[[Node], Tuple[Left, Right]]


def repr_tree(
        node: Node,
        stringify: Stringifier,
        separate: Separator) -> columns.Column:
    '''Returns the string representing tree structure for a given node.

    Args:
        current (Node): Current node to be processed.
        stringify (Stringifier): Function to be called when the node is stringify.
        separator (Separator): Function to be called when the children of the current node is separated.

    Returns:
        Sequence[str]: Human readable string representation of the node.
    '''
    l, r = separate(current)
    formatter = lambda n: repr_tree(n, stringify, separate)
    lcolumn = columns.left(map(formatter, l)) if l else (),
    rcolumn = columns.right(map(formatter, r)) if r else ()
    children = tuple(
        columns.connect(lcolumn, rcolumn) if l or r else ()
    )
    name = stringify(node)
    llen, rlen = columns.get_width(lcolumn), columns.get_width(rcolumn)
    name = f"{' ' * (llen - (len(name) // 2))}{name}{' ' * (rlen - (len(name) // 2))}"
    return columns.combine([[name, *children]])
