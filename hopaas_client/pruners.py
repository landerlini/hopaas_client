import dataclasses
from dataclasses import dataclass
from typing import Union

testables = [
    'NopPruner',
    'HyperbandPruner',
    'MedianPruner',
    'ThresholdPruner'
]


@dataclass(frozen=True)
class Pruner:
    def asdict(self):
        return dict(
            name=self.__class__.__name__,
            args=dataclasses.asdict(self)
        )


@dataclass(frozen=True)
class NopPruner(Pruner):
    pass


@dataclass(frozen=True)
class HyperbandPruner(Pruner):
    min_resources: int = 1
    max_resources: Union[str, int] = 'auto'
    bootstrap_count: int = 0


@dataclass(frozen=True)
class MedianPruner(Pruner):
    n_startup_trials: int = 5
    n_warmup_steps: int = 0
    interval_steps: int = 1
    n_min_trials: int = 1


@dataclass(frozen=True)
class ThresholdPruner(Pruner):
    lower: Union[float, None] = None
    upper: Union[float, None] = None
    n_warmup_steps: int = 0
    interval_steps: int = 1
