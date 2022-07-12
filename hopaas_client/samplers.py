import dataclasses
from dataclasses import dataclass

testables = [
    'TPESampler'
]


@dataclass(frozen=True)
class Sampler:
    def asdict(self):
        return dict(
            name=self.__class__.__name__,
            args=dataclasses.asdict(self)
        )


@dataclass(frozen=True)
class TPESampler(Sampler):
    n_startup_trials: int = 10
    n_ei_candidates: int = 24
    consider_magic_clip: bool = True

