"""Convert breath events to kepathian events"""

from mutwo import breath_converters
from mutwo import breath_events
from mutwo import core_converters
from mutwo import core_events
from mutwo import music_converters
from mutwo import kepathian_converters
from mutwo import kepathian_events


__all__ = (
    "BreathTimeToKValue",
    "BreathCellToKCell",
    "BreathValueToKValue",
    "BreathSequenceToKTable",
)


class BreathTimeToKValue(core_converters.abc.Converter):
    def convert(self, breath_time: breath_events.BreathTime) -> kepathian_events.KValue:
        return (
            core_events.SimpleEvent(breath_converters.constants.BREATH_DURATION)
            .set("value", breath_time.breath.symbol)
            .set("width", breath_converters.configurations.DEFAULT_BREATH_VALUE_WIDTH)
        )


class BreathValueToKValue(core_converters.abc.Converter):
    """A note to a kepathian note"""

    e2pitch_list = music_converters.SimpleEventToPitchList()
    mp2kp = kepathian_converters.MutwoPitchToKepathianPitch()

    def convert(
        self, breath_value: breath_events.BreathValue
    ) -> kepathian_events.KValue:
        pitch_list = self.e2pitch_list(breath_value)
        kpitch = self.mp2kp(pitch_list[0]) if pitch_list else ""
        kvalue = (
            core_events.SimpleEvent(breath_value.duration)
            .set("value", kpitch)
            .set("width", breath_converters.configurations.DEFAULT_BREATH_VALUE_WIDTH)
        )
        return kvalue


class BreathCellToKCell(core_converters.abc.Converter):
    """A sequence of notes during one breath to a kepathian notes sequence"""

    def __init__(
        self, breath_value_to_kvalue: BreathValueToKValue = BreathValueToKValue()
    ):
        self.bvalue2kvalue = breath_value_to_kvalue

    def convert(self, breath_cell: breath_events.BreathCell) -> kepathian_events.KCell:
        return core_events.SequentialEvent(
            [self.bvalue2kvalue(bv) for bv in breath_cell]
        )


class BreathSequenceToKTable(core_converters.abc.Converter):
    def __init__(
        self,
        breath_time_to_kvale: BreathTimeToKValue = BreathTimeToKValue(),
        breath_cell_to_kcell: BreathCellToKCell = BreathCellToKCell(),
    ):
        self.b2kvalue = breath_time_to_kvale
        self.bcell2kcell = breath_cell_to_kcell

    def convert(
        self, breath_sequence: breath_events.BreathSequence
    ) -> kepathian_events.KTable:
        r = breath_converters.breath_sequence_to_row_name_tuple(breath_sequence)
        ktable = core_events.SimultaneousEvent(
            [
                core_events.TaggedSequentialEvent(
                    [], tag=breath_converters.constants.BREATH_TAG
                )
            ]
            + [core_events.TaggedSequentialEvent([], tag=n) for n in r]
        )
        for b in breath_sequence:
            ktable[breath_converters.constants.BREATH_TAG].append(
                core_events.SequentialEvent([self.b2kvalue(b)])
            )
            # A breath is one cell, so we append the events.
            for e in b:
                ktable[e.tag].append(self.bcell2kcell(e))
        return ktable
