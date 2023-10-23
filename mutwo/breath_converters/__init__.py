from mutwo import breath_events
from mutwo import core_converters
from mutwo import core_events
from mutwo import kepathian_events

from . import constants


class BreathTimeToKValue(core_converters.abc.Converter):
    def convert(self, breath_time: breath_events.BreathTime) -> kepathian_events.KValue:
        return core_events.SimpleEvent(constants.BREATH_DURATION).set(
            'value', breath_time.breath.symbol
        )


class BreathSequenceToKTable(core_converters.abc.Converter):
    def __init__(self, breath_time_to_kvale: BreathTimeToKValue = BreathTimeToKValue()):
        self.b2kvalue = breath_time_to_kvale

    def convert(
        self, breath_sequence: breath_events.BreathSequence
    ) -> kepathian_events.KTable:
        r = breath_sequence_to_row_name_tuple(breath_sequence)
        ktable = core_events.SimultaneousEvent(
            [core_events.TaggedSequentialEvent([], tag=constants.BREATH_TAG)]
            + [core_events.TaggedSequentialEvent([], tag=n) for n in r]
        )
        for b in breath_sequence:
            ktable[constants.BREATH_TAG].append(
                core_events.SequentialEvent([self.b2kvalue(b)])
            )
            # A breath is one cell, so we append the events.
            for e in b:
                ktable[e.tag].append(e)
        return ktable


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
