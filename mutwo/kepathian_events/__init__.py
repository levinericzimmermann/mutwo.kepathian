"""Define events to represent a table of cipher notation (aka kepathian).

Cipher notation tables may look like this:

  1  |  2  |  3  |  4
a  b |  cd |  e  |fg

In mutwo.kepathian they are described by the following events:
"""

import typing

from mutwo import core_events

KValue: typing.TypeAlias = core_events.abc.Event
"""A :class:`KValue` is one item in a cell.

In a table like

  1  |  2  |  3  |  4
a  b |  cd |  e  |fg

are

    - a
    - b
    - c
    - d
    - e
    - f
    - g

all represented as :class:`KValue`.
Each :class:`Kvalue` resides in a :class:`KCell`.
"""

KCell: typing.TypeAlias = core_events.SequentialEvent[KValue]
"""A :class:`KCell` is one data entry in a table.

In a table like

  1  |  2  |  3  |  4
a  b |  cd |  e  |fg

are

    - | a b |
    - |  cd |
    - |  e  |
    - |fg   |

all represented as :class:`KCell`.
Basically :class:`KCell` are a sequence of :class:`KValue`.
Each :class:`KCell` resides in a `KRow`.
"""


KRow: typing.TypeAlias = core_events.SequentialEvent[KCell]
"""A :class:`KRow` is one row of a table.

In a table like

  1  |  2  |  3  |  4
a  b |  cd |  e  |fg

is

    - a  b |  cd |  e  |fg

represented as one :class:`KRow`.
Basically :class:`KRow` are a sequence of :class:`KCell`.
Each :class:`KRow` resides in a `KTable`.
"""

KTable = typing.TypeAlias = core_events.SimultaneousEvent[KRow]
"""A :class:`KTable` represents one full table."""

del core_events, typing
