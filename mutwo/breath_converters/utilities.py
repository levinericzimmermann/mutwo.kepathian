"""Utilities for breath converters"""

from mutwo import breath_events

__all__ = ("breath_sequence_to_row_name_tuple",)


def breath_sequence_to_row_name_tuple(
    breath_sequence: breath_events.BreathSequence,
) -> tuple[str, ...]:
    def b2r(b: breath_events.BreathTime):
        return tuple(e.tag for e in b)

    b0 = breath_sequence[0]
    r = b2r(b0)
    for b in breath_sequence[1:]:
        assert b2r(b) == r, "Missing parts"
    return r
