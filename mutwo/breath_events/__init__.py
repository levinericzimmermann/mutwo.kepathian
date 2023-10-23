from mutwo import breath_parameters
from mutwo import core_events
from mutwo import music_events


class BreathTime(
    # We host different singers/whistlers/instruments in one breath
    core_events.SimultaneousEvent[
        # Each of these singers/whistlers/instruments plays a sequence of
        # notes or rests.
        core_events.TaggedSequentialEvent[
            core_events.SimpleEvent | music_events.NoteLike
        ]
    ]
):
    def __init__(
        self,
        *args,
        breath: breath_parameters.Breath = breath_parameters.Breath(),
        **kwargs
    ):
        self.breath = breath
        super().__init__(*args, **kwargs)


class BreathSequence(core_events.SequentialEvent[BreathTime]):
    """A sequence of breaths"""
