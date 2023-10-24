from mutwo import core_converters
from mutwo import music_parameters

__all__ = ("MutwoPitchToKepathianPitch",)


class MutwoPitchToKepathianPitch(core_converters.abc.Converter):
    def convert(self, pitch: music_parameters.abc.Pitch) -> str:
        try:
            # WesternPitch?
            return pitch.name
        except AttributeError:
            try:
                # ScalePitch?
                return str(pitch.scale_degree + 1)
            except AttributeError:
                # Ok, let's hope it's any pitch:
                return str(int(round(pitch.frequency)))
