from typing import List
from dataclasses import dataclass


class Suggestion:
    pass


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

    def __str__(self):
        return f"optuna#float({self.min},{self.max})"


@dataclass(frozen=True)
class DiscreteUniform(Suggestion):
    low: float
    high: float = 1
    q: bool = False

    def __str__(self):
        return f"optuna#discrete_uniform({self.low},{self.high},{self.q})"


@dataclass(frozen=True)
class LogUniform(Suggestion):
    low: float
    high: float = 1

    def __str__(self):
        return f"optuna#loguniform({self.low},{self.high})"


@dataclass(frozen=True)
class Categorical(Suggestion):
    choices: List[str]

    def __str__(self):
        return f"optuna#categorical({','.join(self.choices)})"

