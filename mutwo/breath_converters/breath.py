"""Convert breath events to flat musical structures"""

from mutwo import breath_converters
from mutwo import breath_events
from mutwo import core_converters
from mutwo import core_events


__all__ = ("BreathSequenceToSimultaneousEvent",)


class BreathSequenceToSimultaneousEvent(core_converters.abc.Converter):
    def convert(
        self, breath_sequence_to_convert: breath_events.BreathSequence
    ) -> core_events.SimultaneousEvent[core_events.TaggedSequentialEvent]:
        r = breath_converters.breath_sequence_to_row_name_tuple(
            breath_sequence_to_convert
        )
        simultaneous_event = core_events.SimultaneousEvent(
            [core_events.TaggedSequentialEvent([], tag=t) for t in r]
        )
        for breath_time in breath_sequence_to_convert:
            duration = breath_time.breath.duration
            breath_time = breath_time.copy().set("duration", duration)
            for seq in breath_time:
                simultaneous_event[seq.tag].extend(seq)
        return simultaneous_event
