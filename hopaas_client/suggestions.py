from typing import List, Optional
from dataclasses import dataclass


class Suggestion:
    pass


# FIXME : deprecated in Optuna v3.0.0, use 'suggest_float()' instead
@dataclass(frozen=True)
class Uniform(Suggestion):
    min: float
    max: float

    def __str__(self):
        return f"optuna#uniform({self.min},{self.max})"


@dataclass(frozen=True)
class Int(Suggestion):
    min: int
    max: int
    step: int = 1
    log: bool = False

    def __str__(self):
        return f"optuna#int({self.min},{self.max},{self.step},{str(self.log).lower()})"


@dataclass(frozen=True)
class Float(Suggestion):
    min: float
    max: float
    # step: Optional[float] = None
    # log: bool = False

    def __str__(self):
        # return f"optuna#float({self.min},{self.max},{self.step},{self.log})"
        return f"optuna#float({self.min},{self.max})"


# FIXME : deprecated in Optuna v3.0.0, use 'suggest_float()' instead
@dataclass(frozen=True)
class DiscreteUniform(Suggestion):
    low: float
    high: float
    # q: float

    def __str__(self):
        # return f"optuna#discrete_uniform({self.low},{self.high},{self.q})"
        return f"optuna#discrete_uniform({self.low},{self.high})"


# FIXME : deprecated in Optuna v3.0.0, use 'suggest_float()' instead
@dataclass(frozen=True)
class LogUniform(Suggestion):
    low: float
    high: float

    def __str__(self):
        return f"optuna#loguniform({self.low},{self.high})"


@dataclass(frozen=True)
class Categorical(Suggestion):
    choices: List[str]

    def __str__(self):
        return f"optuna#categorical({','.join(self.choices)})"
