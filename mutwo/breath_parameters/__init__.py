import enum


class BreathDirection(enum.Enum):
    INHALE = 0
    EXHALE = 1


class BreathSpeed(enum.Enum):
    SLOW = 0
    FAST = 1


class Breath(object):
    def __init__(
        self,
        direction: BreathDirection = BreathDirection.INHALE,
        speed: BreathSpeed = BreathSpeed.SLOW,
    ):
        self.direction = direction
        self.speed = speed

    @property
    def symbol(self) -> str:
        d, s = BreathDirection, BreathSpeed
        key = (self.direction, self.speed)
        match key:
            case (d.INHALE, s.SLOW):
                return "⇑"
            case (d.INHALE, s.FAST):
                return "↑"
            case (d.EXHALE, s.SLOW):
                return "⇓"
            case (d.EXHALE, s.FAST):
                return "↓"
            case _:
                raise NotImplementedError(key)
