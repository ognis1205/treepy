from enum import Enum
from itertools import (
    chain,
    repeat,
    zip_longest
)
from typing import (
    Sequence,
    Tuple,
    Optional,
)


class Connectors(str, Enum):
    NULL = ' ' * 3
    EDGE = '─' * 3
    LCORNER = ' ┌─'
    RCORNER = '─┐ '
    LBRANCH = '─┘ '
    RBRANCH = ' └─'
    DTSHAPE = '─┬─'
    UTSHAPE = '─┴─'


Column = Sequence[str]


def get_width(column: Column) -> int:
    if not column:
        return 0
    return max(map(len, column), default=0)
#    return len(column[0])


def combine(columns: Sequence[Column], joiners: Sequence[str] = ()) -> Column:
    '''Takes one list of strings or more and joins them line by line with the specified joiners.

    Args:
        columns (Sequence[Column]): [['a', ...], ['b', ...], ...]
        joiners (Tuple[str, ...]): ['─', ...]

    Returns:
        Column: ['a-b-...', ...]
    '''
    widths = tuple(get_width(c) for c in columns)
    return tuple(
        joiner.join(
            row.center(width)
            for row, width in zip(rows, widths)
        ) for rows, joiner in zip(zip_longest(*columns, fillvalue=''), chain(joiners, repeat(f'{Connectors.NULL}')))
    )


def _link(
        connector: Connectors,
        column: Column,
        lspace: Optional[int] = None,
        rspace: Optional[int] = None) -> Column:
    '''Links a given column with a specified connector.

    Args:
        connector (Connectors): Connector string for a given column.
        column (Column): ['a', ...]
        lspace (Optional[int]): Number of spaces for the left space of a specified connector.
        rspace (Optional[int]): Number of spaces for the right space of a specified connector.

    Returns:
        Column: ['─┐ ', 'a', ...]
    '''
    l = ' ' if connector == Connectors.LCORNER else '─'
    r = ' ' if connector == Connectors.RCORNER else '─'
    if not (lspace or rspace):
        width = get_width(column)
        if width:
            width -= 1
        lspace = width // 2
        rspace = width - lspace
    return combine([[
        f'{l * lspace}{connector}{r * rspace}',
        *column
    ]])


def _branches(columns: Sequence[Column]) -> Column:
    '''Draws given columns as junctions.

    Args:
        columns (Sequence[Column]): [['a', ...], ['b', ...], ...]

    Returns:
        Column: ['─┬─┬─, ...', ' a b ...', ...]
    '''
    return combine(
        tuple(map(lambda c: _link(Connectors.DTSHAPE, c), columns)),
        (f'{Connectors.EDGE}',)
    )


def left(columns: Sequence[Column]) -> Column:
    '''Draws given columns as left nodes.

    Args:
        columns (Sequence[Column]): [['a', ...], ['b', ...], ...]

    Returns:
        Column: [' ┌─┬─, ...', ' a b ...', ...]
    '''
    head, *tail = columns
    return combine(
        [_link(Connectors.LCORNER, head), _branches(tail)],
        (f'{Connectors.EDGE}',)
    )


def right(columns: Sequence[Column]) -> Column:
    '''Draws given columns as right nodes.

    Args:
        columns (Sequence[Column]): [['a', ...], ['b', ...], ...]

    Returns:
        Column: ['..., ─┬─┐ ', '... y z ', ...]
    '''
    *head, tail = columns
    return combine(
        [_branches(head), _link(Connectors.RCORNER, tail)],
        (f'{Connectors.EDGE}',)
    )


def connect(left: Column, right: Column) -> Column:
    '''Draws given columns as right nodes.

    Args:
        columns (Sequence[Column]): [[' ┌─┬─, ...', ' a b ...', ...], ['..., ─┬─┐ ', '... c d ', ...], ...]

    Returns:
        Column: [' ┌─┬─┴─┬─┐ ', ' a b   c d ', ...]
    '''
    return combine(
        [left, right],
        ((Connectors.UTSHAPE if right else Connectors.LBRANCH) if left else Connectors.RBRANCH,)
    )
