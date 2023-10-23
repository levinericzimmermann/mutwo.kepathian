from mutwo import core_converters
from mutwo import music_parameters

__all__ = ("MutwoPitchToKepathianPitch",)


class MutwoPitchToKepathianPitch(core_converters.abc.Converter):
    def convert(self, pitch: music_parameters.abc.Pitch) -> str:
        try:
            return pitch.name
        except AttributeError:
            return int(round(pitch.frequency))
